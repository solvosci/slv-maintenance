# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    maintenance_request_open_user_ids = fields.Many2many(
        comodel_name="res.partner",
        related="company_id.maintenance_request_open_user_ids",
        string="Notify contacts for open request",
        readonly=False
    )
    
class ResCompany(models.Model):
    _inherit = "res.company"
    
    maintenance_request_open_user_ids = fields.Many2many(
        "res.partner", 
        string="Notify contacts for open request"
    )
