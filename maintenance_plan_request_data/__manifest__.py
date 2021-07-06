# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Maintenance Plan Request related data",
    "summary": "Adds new fields to Maintenance Request related to Plans",
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "12.0.1.0.0",
    "category": "Maintenance",
    "website": "https://github.com/solvosci/slv-maintenance",
    "depends": [
        "maintenance_plan",
    ],
    "data": [
        "views/maintenance_request_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
