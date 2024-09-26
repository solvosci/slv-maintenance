# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Maintenance Plan with meter mode",
    "summary": """
        Maintenance plan by self-increasing meter.
        Adds new mode: meter mode. 
        When meter mode is true you have to configure autoincrement params.
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "12.0.1.0.0",
    "category": "Maintenance",
    "website": "https://github.com/solvosci/slv-maintenance",
    "depends": [
        'maintenance_plan', 'uom'
    ],
    "data": [
        "views/maintenance_views.xml",
    ],
    'demo': [
        'data/demo_maintenance_plan_meter_mode.xml',
    ],
    'installable': True,
}
