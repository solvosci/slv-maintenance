# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Maintenance Request IFS check",
    "summary": """
        Adds IFS check to maintenance request.
        4 checks:
            - equipment repaired correctly
            - free strange elements
            - collected location
            - cleaning the area
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
        "views/maintenance_views.xml",
    ],
    'installable': True,
}
