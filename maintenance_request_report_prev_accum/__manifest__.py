# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Maintenance Request Accumulated Preventive Report",
    "summary": """
        Adds a report for accumulated data of Preventive Requests
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "12.0.1.0.0",
    "category": "Maintenance",
    "website": "https://github.com/solvosci/slv-maintenance",
    "depends": [
        "maintenance_plan",
        "maintenance_request_time_performance",
        "report_xlsx",
    ],
    "data": [
        "report/report_prev_accum.xml",
        "wizard/report_prev_accum_wizard.xml",
    ],
    'installable': True,
}
