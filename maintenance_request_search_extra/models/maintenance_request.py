# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import api, fields, models


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    schedule_day = fields.Date(
        compute='_compute_schedule_day',
        store=True)

    @api.depends('schedule_date')
    def _compute_schedule_day(self):
        for req in self:
            req.schedule_day = req.schedule_date and req.schedule_date.date()
