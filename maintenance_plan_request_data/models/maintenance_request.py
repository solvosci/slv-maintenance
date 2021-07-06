# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import api, fields, models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    calc_maintenance_plan_id = fields.Many2one(
        comodel_name="maintenance.plan",
        string="Calculated Maintenance Plan",
        help="For preventive requests, obtains the possible related plan,"
        " if possible. It's useful for maintenance_plan implementations"
        " that have unlinked requests",
        readonly=True,
    )
    plan_period = fields.Integer(
        related="calc_maintenance_plan_id.period",
        string="Plan Period",
        store=True,
    )

    @api.multi
    def _recompute_calc_maintenance_plan_id(self):
        """
        If a request is not initially linked, or the request was not
        created within cron, calling this method could recompute it
        """
        plan_obj = self.env["maintenance.plan"]
        for record in self.filtered(
            lambda r: r.maintenance_type == "preventive"
        ):
            record.calc_maintenance_plan_id = plan_obj.search([
                ("equipment_id", "=", record.equipment_id.id),
                ("maintenance_kind_id", "=", record.maintenance_kind_id.id),
            ], limit=1) or False
