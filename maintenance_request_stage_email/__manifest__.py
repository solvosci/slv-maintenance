# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Maintenance Request Stage Email",
    "summary": """
        Adds automatic email sending when creating and closing a maintenance request.
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "12.0.1.0.0",
    "category": "Maintenance",
    "website": "https://github.com/solvosci/slv-maintenance",
    "depends": [
        'base_maintenance_config',
    ],
    "data": [
        "views/maintenance_views.xml",
        "views/maintenance_request_template.xml",
    ],
    'installable': True,
}
