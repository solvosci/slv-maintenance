# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
from odoo import models, api


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    @api.model
    def create(self, vals):
        request = super().create(vals)
        if request.company_id.maintenance_request_open_user_ids:
            request_users = request.company_id.maintenance_request_open_user_ids
            for user in request_users.filtered(lambda x: x.email):
                values = {"user_notify_id": user.id, "user_notify_email": user.email}
                template = self.env.ref('maintenance_request_stage_email.maintenance_request_created_email_template')
                template.with_context(values).send_mail(request.id, email_values=None, force_send=True)
        return request

    @api.multi
    def write(self, values):
        requests = self.filtered(
            lambda r: not r.stage_id.done and r.equipment_id.users_notify_closed_ids
        )
        res = super().write(values)
        if requests and values.get("stage_id", False):
            new_stage_id = self.env["maintenance.stage"].browse(
                values.get("stage_id")
            )
            if new_stage_id.done:
                template = self.env.ref(
                    "maintenance_request_stage_email.maintenance_request_closed_email_template"
                )
                for record in requests:
                    for user in record.equipment_id.users_notify_closed_ids:
                        tmpl_vals = {"user_notify_id": user.id, "user_notify_email": user.email}
                        template.with_context(tmpl_vals).send_mail(
                            record.id, email_values=None, force_send=True
                        )

        return res
