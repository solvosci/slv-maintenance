# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Maintenance Request time performance",
    "summary": """
        Adds start and end date and time of maintenance request completion.
        Adds the difference between real and theoretical completion time.
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "12.0.1.0.0",
    "category": "Maintenance",
    "website": "https://github.com/solvosci/slv-maintenance",
    "depends": [
        'maintenance'
    ],
    "data": [
        "data/maintenance_data.xml",
        "views/maintenance_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    'installable': True,
}
