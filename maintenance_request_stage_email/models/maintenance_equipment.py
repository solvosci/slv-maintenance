# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
from odoo import fields, models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"
    
    users_notify_closed_ids = fields.Many2many(
        "res.partner", 
        string="Notify Contacts for closed request"
    )
