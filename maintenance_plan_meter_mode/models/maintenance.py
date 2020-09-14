# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class MaintenanceEquipment(models.Model):

    _inherit = 'maintenance.equipment'

    maintenance_meter_mode_plan_ids = fields.One2many(
        string='Maintenance meter mode plan',
        comodel_name='maintenance.plan',
        inverse_name='equipment_id',
        domain=[('meter_mode','=',True)]
    )

class MaintenancePlan(models.Model):
    _inherit = 'maintenance.plan'

    meter_mode = fields.Boolean(
        string='Meter mode')
    meter_current_value = fields.Float(
        string='Current value',
        help="This field can be updated manually or "
             "daily adding a value defined.")
    meter_autoinc_mode = fields.Boolean(
        string='Auto incremental mode',
        help="If checked, Current value is periodically incremented according"
            " a self-increase value; otherwise only manual changes of"
            " Current value are allowed")
    meter_autoinc_value = fields.Float(
        string='Value to self-increase per day')
    meter_autoinc_unit = fields.Many2one(
        'uom.uom',
        string='Unit of Value to self-increase per day')
    meter_autoinc_maxvalue = fields.Float(
        string='Interval between requests',
        help='Increment since the last revision to generate another request')
    meter_autoinc_lastvalue = fields.Float(
        string='Value of last revision',
        help='Value from which the last revision was made')
    meter_autoinc_lastupdate = fields.Date(
        string='Date of last revision',
        readonly=True)

    def _compute_next_maintenance(self):
        super()._compute_next_maintenance()

        for plan in self.filtered(lambda x: x.meter_mode):
            next_maintenance_todo = self.env['maintenance.request'].search([
                ('equipment_id', '=', plan.equipment_id.id),
                ('maintenance_type', '=', 'preventive'),
                ('maintenance_kind_id', '=', plan.maintenance_kind_id.id),
                ('maintenance_plan_id', '=', plan.id),
                ('stage_id.done', '!=', True),
                ('close_date', '=', False)], order="request_date asc", limit=1)

            plan.next_maintenance_date = next_maintenance_todo.request_date \
                if next_maintenance_todo else plan.start_maintenance_date

    @api.onchange('meter_mode')
    def _onchange_meter_mode(self):
        if self.meter_mode:
            self.interval = None
            self.interval_step = None
            self.maintenance_plan_horizon = None
            self.planning_step = None
        else:
            self.meter_current_value = None
            self.meter_autoinc_mode = None
            self.meter_autoinc_value = None
            self.meter_autoinc_unit = None
            self.meter_autoinc_maxvalue = None
            self.meter_autoinc_lastvalue = None
            self.meter_autoinc_lastupdate = None

    @api.onchange('meter_autoinc_mode')
    def _onchange_meter_mode(self):
        if not self.meter_autoinc_mode:
            self.meter_autoinc_value = 0
            self.meter_autoinc_unit = False

    @api.constrains(
        'meter_mode', 
        'meter_autoinc_mode', 
        'meter_autoinc_value', 
        'meter_autoinc_unit', 
        'meter_autoinc_maxvalue')
    def _check_meter_mode(self):
        for plan in self:
            if plan.meter_mode:
                if self.meter_autoinc_mode and \
                        (not plan.meter_autoinc_value or not plan.meter_autoinc_unit):
                    raise ValidationError(
                        _("Cannot set auto incremental Meter mode"
                          " without Value to self-increase per day"))
                if not plan.meter_autoinc_maxvalue:
                    raise ValidationError(
                        _("It can´t be Meter mode"
                          " without Maximum amount since the last revision"))

    def _review_meter_mode_values(self, values):
        meter_mode = values['meter_mode'] \
            if 'meter_mode' in values else self.meter_mode
        meter_autoinc_mode = values['meter_autoinc_mode'] \
            if 'meter_autoinc_mode' in values else self.meter_autoinc_mode
        if meter_mode:
            values['interval'] = None
            values['interval_step'] = None
            values['maintenance_plan_horizon'] = None
            values['planning_step'] = None
            if not meter_autoinc_mode:
                values['meter_autoinc_value'] = 0
        else:
            values['meter_current_value'] = None
            values['meter_autoinc_mode'] = None
            values['meter_autoinc_value'] = None
            values['meter_autoinc_unit'] = None
            values['meter_autoinc_maxvalue'] = None
            values['meter_autoinc_lastvalue'] = None
            values['meter_autoinc_lastupdate'] = None
        return values

    @api.model
    def create(self, values):
        values = self._review_meter_mode_values(values)
        return super(MaintenancePlan, self).create(values)

    @api.multi
    def write(self, values):
        values = self._review_meter_mode_values(values)
        return super(MaintenancePlan, self).write(values)


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    @api.model
    def _cron_generate_requests(self):
        super()._cron_generate_requests()
        # Generates maintenance request on the next_maintenance_date
        for plan in self.env['maintenance.plan'].search(
                [('meter_mode', '=', True)]):
            equipment = plan.equipment_id
            equipment._create_new_request_meter_mode(plan)

    def _create_new_request_meter_mode(self, mp):
        # Compute meter_current_value adding meter_autoinc_value from last day
        if not mp.meter_autoinc_lastupdate:
            mp.meter_autoinc_lastupdate = fields.Date.today()
        if mp.meter_autoinc_lastupdate < fields.Date.today():
            diff = fields.Date.today() - mp.meter_autoinc_lastupdate
            mp.meter_current_value += mp.meter_autoinc_value * diff.days
            mp.meter_autoinc_lastupdate = fields.Date.today()

        # Create maintenance request if current value is greater than autoinc value
        requests = self.env['maintenance.request']
        meter_value = mp.meter_autoinc_maxvalue+mp.meter_autoinc_lastvalue
        if mp.meter_current_value >= meter_value:
            # We check maintenance request already created
            furthest_maintenance_todo = self.env['maintenance.request'].search(
                [('maintenance_plan_id', '=', mp.id)],
                order="request_date desc", limit=1)
            if furthest_maintenance_todo:
                next_maintenance_date = furthest_maintenance_todo.request_date
            else:
                next_maintenance_date = mp.next_maintenance_date
            # Create maintenance request
            if not next_maintenance_date \
                    or next_maintenance_date < fields.Date.today():
                mp.meter_autoinc_lastvalue = mp.meter_current_value
                vals = self._prepare_request_from_plan(
                    mp, fields.Date.today()
                )
                requests |= self.env['maintenance.request'].create(vals)
        return requests
