# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    maintenance_equipment_ids = fields.Many2many("maintenance.equipment", string="Maintenance equipments")
