# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    def _prepare_request_from_plan(self, maintenance_plan):
        req = super()._prepare_request_from_plan(maintenance_plan)
        req["calc_maintenance_plan_id"] = maintenance_plan.id
        return req
