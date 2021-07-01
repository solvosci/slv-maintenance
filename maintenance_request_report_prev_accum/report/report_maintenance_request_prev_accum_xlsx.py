# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
from odoo import _, models
from odoo.tools import format_date

from base64 import b64decode
from tempfile import NamedTemporaryFile


class ReportPrevAccumXlsx(models.TransientModel):
    _name = "report.maintenance_request_p_a_report_xlsx"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, accumdata):
        sheet = workbook.add_worksheet("Requests summary")

        formats = {
            "title": workbook.add_format({'bold': True, 'size': 30}),
            "header": workbook.add_format({'bold': True, 'align': 'center'}),
            "normal": workbook.add_format({
                'align': 'center', 'num_format': '0'
            }),
            "pct": workbook.add_format({
                'align': 'center', 'num_format': '0.00%'
            }),
        }

        sheet.set_column('A:A', 20)
        sheet.set_column('B:H', 12)

        binary_logo = self.env.user.company_id.logo_web
        if binary_logo:
            fp = NamedTemporaryFile(delete=False)
            fp.write(bytes(b64decode(binary_logo)))
            fp.close()
            sheet.insert_image("A1", fp.name, {
                'x_offset': 18, 'y_offset': 18, 'x_scale': 0.9, 'y_scale': 0.5
            })

        sheet.write(1, 2, _("Requests Accumulative Summary"), formats["title"])

        row = 5
        sheet.write(row, 0, _("Company"), formats["header"])
        sheet.write(row, 1, _("From"), formats["header"])
        sheet.write(row, 2, _("To"), formats["header"])
        sheet.write(row, 3, _("Req. Done"), formats["header"])
        sheet.write(row, 4, _("Not late"), formats["header"])
        sheet.write(row, 5, _("Scheduled"), formats["header"])
        sheet.write(row, 6, _("% Done"), formats["header"])
        sheet.write(row, 7, _("% Not late"), formats["header"])
        for accum in accumdata:
            row = row + 1
            sheet.write(
                row,
                0,
                _("ALL") if not accum.company_id else accum.company_id.name,
                formats["normal"],
            )
            sheet.write(row, 1, format_date(
                self.env, accum.date_from
            ), formats["normal"])
            sheet.write(row, 2, format_date(
                self.env, accum.date_to
            ), formats["normal"])
            sheet.write(row, 3, accum.requests_done, formats["normal"])
            sheet.write(row, 4, accum.requests_done_not_late, formats["normal"])
            sheet.write(row, 5, accum.requests_scheduled, formats["normal"])
            sheet.write(row, 6, accum.requests_done_pct, formats["pct"])
            sheet.write(
                row, 7, accum.requests_done_not_late_pct, formats["pct"]
            )
