# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
from odoo import api, fields, models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    done_late = fields.Boolean(
        default=False,
        compute="_compute_done_late",
        help="Indicates if request, if done, "
        "was finished after the next planned one",
    )

    @api.multi
    def _compute_done_late(self):
        model = self.env["maintenance.request"]
        # Only linked to a plan done requests could be late
        # This code is only valid starting with Maintenance Plan 12.0.2.3.0,
        #  and for the subsequent requests after updating addon
        #
        # for record in self.filtered(
        #     lambda r: r.maintenance_plan_id and r.stage_id.done
        # ):
        #     overlapped_requests = model.search([
        #         ("equipment_id", "=", record.equipment_id.id),
        #         ("maintenance_plan_id", "=", record.maintenance_plan_id.id),
        #         ("request_date", ">", record.schedule_date),
        #         ("request_date", "<", record.end_request_datetime),
        #     ])
        #     record.done_late = (len(overlapped_requests) > 0)
        #
        # Equivalent code, since a kind and plan are linked 1<->1
        for record in self.filtered(
            lambda r: r.maintenance_type == "preventive" and r.stage_id.done
        ):
            overlapped_requests = model.search([
                ("equipment_id", "=", record.equipment_id.id),
                ("maintenance_kind_id", '=', record.maintenance_kind_id.id),
                ("request_date", ">", record.request_date),
                ("request_date", "<", record.end_request_datetime),
            ])
            record.done_late = (len(overlapped_requests) > 0)
