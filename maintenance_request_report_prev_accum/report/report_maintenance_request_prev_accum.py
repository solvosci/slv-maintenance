# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
from odoo import api, fields, models


class ReportPrevAccumXlsx(models.TransientModel):
    _name = "report_maintenance_request_p_a"
    _inherit = "report.report_xlsx.abstract"

    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)
    company_id = fields.Many2one(comodel_name="res.company")
    requests_done = fields.Integer()
    requests_done_not_late = fields.Integer()
    requests_scheduled = fields.Integer()
    requests_done_pct = fields.Float(
        string="% Done",
        compute="_compute_requests_done_pct",
    )
    requests_done_not_late_pct = fields.Float(
        string="% Done not late",
        compute="_compute_requests_done_not_late_pct",
    )

    def _compute_requests_done_pct(self):
        for record in self:
            record.requests_done_pct = (
                record.requests_scheduled and
                (record.requests_done/record.requests_scheduled)
            ) or 0

    def _compute_requests_done_not_late_pct(self):
        for record in self:
            record.requests_done_not_late_pct = (
                record.requests_scheduled and
                (record.requests_done_not_late/record.requests_scheduled)
            ) or 0

    @api.multi
    def compute_data_for_report(self):
        self.ensure_one()
        req_scheduled = self.env["maintenance.request"].search([
            ("maintenance_type", "=", "preventive"),
            ("request_date", ">=", self.date_from),
            ("request_date", "<=", self.date_to),
        ])

        companies = req_scheduled.mapped("company_id")
        self.company_id = (len(companies) == 1 and companies[0]) or False
        self.requests_scheduled = len(req_scheduled)
        self.requests_done = len(req_scheduled.filtered(
            lambda r: r.stage_id.done
        ))
        self.requests_done_not_late = len(req_scheduled.filtered(
            lambda r: r.stage_id.done and not r.done_late
        ))
