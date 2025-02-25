# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, fields, _

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    product_ids = fields.Many2many("product.product")
    count_product_ids = fields.Integer(compute="compute_product_count")

    def compute_product_count(self):
        for record in self:
            record.count_product_ids = len(record.product_ids)
    
    def action_view_products(self):
        action = {
            'name': _('Products'),
            'res_model': 'product.product',
            'type': 'ir.actions.act_window',
            'context':{
                'default_maintenance_equipment_ids': [(4, self.ids)]
            }
        }
        
        if self.count_product_ids == 1:
            action['view_mode'] = 'form'
            action['res_id'] = self.product_ids.id
        else:
            action['view_mode'] = 'tree,form'
            action['domain'] = [('id', "in", self.product_ids.ids)]
        return action
