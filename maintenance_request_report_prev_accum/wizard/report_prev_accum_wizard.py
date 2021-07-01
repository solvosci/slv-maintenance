# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
from odoo import api, fields, models

from datetime import date, timedelta


class ReportPrevAccumWizard(models.TransientModel):
    _name = "maintenance.request.p_a.report.wizard"
    _description = "Maintenance Request Preventive Accumulated Report Wizard"

    def _get_default_date(self, dt_from=True):
        default_date = date.today().replace(day=1) - timedelta(days=1)
        if dt_from:
            default_date = default_date.replace(day=1)
        return default_date

    date_from = fields.Date(
        string="Start Date",
        required=True,
        default=lambda x: x._get_default_date(),
    )
    date_to = fields.Date(
        string="End Date",
        required=True,
        default=lambda x: x._get_default_date(dt_from=False),
    )

    # TODO company/companies

    @api.multi
    def button_export_xlsx(self):
        self.ensure_one()

        # 1) Create and populate transient record model record
        report = self.env["report_maintenance_request_p_a"].create({
            "date_from": self.date_from,
            "date_to": self.date_to,
        })
        report.compute_data_for_report()
        # 2) Call report printing
        return self.env.ref(
            "maintenance_request_report_prev_accum.action_report_prev_accum_xlsx"
        ).report_action(
            report, config=False
        )
