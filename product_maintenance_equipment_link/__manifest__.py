# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)
{
    "name": "Product Maintenance Equipment Link",
    "summary": """
        Link products with maintenance equipment
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "13.0.1.0.0",
    "category": "Human Resources",
    "website": "https://github.com/solvosci/slv-maintenance",
    "depends": [
        "maintenance",
        "product"
    ],
    "data": [
        "views/product_views.xml",
        "views/maintenance_equipment_views.xml"
    ],
    'installable': True
}
