from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        obj_request = env["maintenance.request"]
        obj_request.search([
            ("stage_id.done", "=", False),
            ("calc_maintenance_plan_id", "=", False),
        ])._recompute_calc_maintenance_plan_id()
