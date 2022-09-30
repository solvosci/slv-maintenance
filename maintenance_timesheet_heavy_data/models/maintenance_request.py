# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    timesheet_total_hours = fields.Float(store=True)
