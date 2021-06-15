# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
from odoo import models, api


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    @api.model 
    def create(self, vals):
        request = super().create(vals)
        if self.env.user.company_id.maintenance_request_open_user_ids:
            request_users = self.env.user.company_id.maintenance_request_open_user_ids
            for user in request_users.filtered(lambda x: x.email):
                values = {"user_notify_id": user.id, "user_notify_email": user.email}
                template = self.env.ref('maintenance_request_stage_email.maintenance_request_created_email_template')
                template.with_context(values).send_mail(request.id, email_values=None, force_send=True)
        return request

    @api.constrains('stage_id')
    def _constrains_stage_id(self):
        if self.stage_id.done and self.equipment_id.users_notify_closed_ids:
            request_users = self.equipment_id.users_notify_closed_ids
            for user in request_users.filtered(lambda x: x.email):
                values = {"user_notify_id": user.id, "user_notify_email": user.email}
                template = self.env.ref('maintenance_request_stage_email.maintenance_request_closed_email_template')
                template.with_context(values).send_mail(self.id, email_values=None, force_send=True)
