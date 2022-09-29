# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Maintenance - Heavy Data Performance Enhacements",
    "summary": """
        Makes some adjustments to Maintenance app in some processes affected
        when database has a heavy load
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "12.0.1.0.0",
    "category": "Maintenance",
    "website": "https://github.com/solvosci/slv-maintenance",
    "depends": ["maintenance"],
    "data": ["views/maintenance_equipment_views.xml"],
    'installable': True,
}
