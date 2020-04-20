from odoo import api, models, fields, _
from datetime import timedelta
from odoo.exceptions import ValidationError


class MaintenanceStage(models.Model):
    _inherit = 'maintenance.stage'

    in_progress = fields.Boolean(
        'In Progress',
        default=False)

    @api.constrains('in_progress', 'done')
    def check_maintenance_stage(self):
        if self.in_progress and self.done:
            raise ValidationError(
                _("It can´t be in progress and done at the same time"))


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    start_request_datetime = fields.Datetime(
        string='Started at',
        help='Start Date and time of maintenance request completion')
    start_request_date = fields.Date(
        compute='_compute_start_request_date',
        string='Start Date of maintenance request completion',
        store=True)
    start_request_datetime_required = fields.Boolean(
        compute='_compute_start_request_datetime_required')
    end_request_datetime = fields.Datetime(
        string='Finished at',
        help='End Date and time of maintenance request completion')
    end_request_date = fields.Date(
        compute='_compute_end_request_date',
        string='End Date of maintenance request completion',
        store=True)
    end_request_datetime_required = fields.Boolean(
        compute='_compute_end_request_datetime_required')
    real_request_duration = fields.Float(
        compute='_compute_real_request_duration',
        string='Real Duration',
        store=True)
    duration_difference = fields.Float(
        compute='_compute_duration_difference',
        string='Difference Duration',
        store=True)
    completion_delay = fields.Float(
        compute='_compute_completion_delay',
        store=True)

    @api.depends('start_request_datetime')
    def _compute_start_request_date(self):
        for req in self:
            req.start_request_date = \
                req.start_request_datetime and \
                req.start_request_datetime.date()

    def _compute_start_request_datetime_required(self):
        for req in self:
            req.start_request_datetime_required = \
                req.stage_id.done or req.stage_id.in_progress

    @api.depends('end_request_datetime')
    def _compute_end_request_date(self):
        for req in self:
            req.end_request_date = \
                req.end_request_datetime and \
                req.end_request_datetime.date()

    def _compute_end_request_datetime_required(self):
        for req in self:
            req.end_request_datetime_required = req.stage_id.done

    @api.depends('start_request_datetime', 'end_request_datetime')
    def _compute_real_request_duration(self):
        for req in self:
            total_hours = 0
            if req.start_request_datetime and req.end_request_datetime \
                    and req.start_request_datetime < req.end_request_datetime:
                diff = req.end_request_datetime - req.start_request_datetime
                total_hours = diff.total_seconds() / 3600
            req.real_request_duration = total_hours

    @api.depends('duration', 'real_request_duration')
    def _compute_duration_difference(self):
        for req in self:
            difference = 0
            if req.duration and req.real_request_duration:
                difference = req.real_request_duration - req.duration
            req.duration_difference = difference

    @api.depends('schedule_date',
                 'duration',
                 'start_request_datetime',
                 'end_request_datetime')
    def _compute_completion_delay(self):
        for req in self:
            diff = None
            if req.end_request_datetime:
                schedule_dt = (req.schedule_date
                               or req.start_request_datetime)
                if schedule_dt.hour == 0 \
                        and schedule_dt.minute == 0 \
                        and schedule_dt.second == 0 \
                        and req.start_request_datetime:
                    # if has no time we put the start_request time
                    schedule_dt = schedule_dt.replace(
                        hour=req.start_request_datetime.hour,
                        minute=req.start_request_datetime.minute,
                        second=req.start_request_datetime.second)
                if req.duration:
                    # add theoretical duration to schedule_date
                    schedule_dt = schedule_dt + timedelta(hours=req.duration)
                diff = req.end_request_datetime - schedule_dt
            req.completion_delay = diff and (diff.total_seconds() / 3600)

    @api.constrains('start_request_datetime', 'end_request_datetime')
    def _check_maintenance_request_task_datetimes(self):
        for req in self:
            if not req.start_request_datetime and req.end_request_datetime:
                raise ValidationError(
                    _("It can´t be End task completion"
                      " without Start task completion"))
            if req.start_request_datetime and req.end_request_datetime \
                    and (req.start_request_datetime
                         > req.end_request_datetime):
                raise ValidationError(
                    _("End task completion cannot be prior to"
                      " Start task completion"))

    @api.onchange('stage_id')
    @api.constrains('stage_id')
    def _compute_request_datetimes(self):
        for req in self:
            if req.stage_id:
                # if stage changes to in_progress ->
                #  fill start_request_datetime
                if req.stage_id.in_progress \
                        and not req.start_request_datetime:
                    req.start_request_datetime = fields.Datetime.now()
                # if stage changes to done stage -> fill end_request_datetime
                if req.stage_id.done and not req.end_request_datetime:
                    # Prevent if request never pass in_progress state
                    if not req.start_request_datetime:
                        req.start_request_datetime = fields.Datetime.now()
                    req.end_request_datetime = fields.Datetime.now()
