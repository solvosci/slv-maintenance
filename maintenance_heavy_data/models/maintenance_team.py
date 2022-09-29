# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html

from odoo import api, models


class MaintenanceTeam(models.Model):
    _inherit = "maintenance.team"

    @api.one
    def _compute_todo_requests(self):
        """
        Overwrites default method, which is extremely slow with large number
        of requests
        """
        obj_mr = self.env['maintenance.request']
        base_domain = [('maintenance_team_id', '=', self.id), ('stage_id.done', '=', False)]
        self.todo_request_ids = obj_mr.search(base_domain)
        self.todo_request_count = len(self.todo_request_ids)
        self.todo_request_count_date = obj_mr.search_count(base_domain + [('schedule_date', '!=', False)])
        self.todo_request_count_high_priority = obj_mr.search_count(base_domain + [('priority', '=', '3')])
        self.todo_request_count_block = obj_mr.search_count(base_domain + [('kanban_state', '=', 'blocked')])
        self.todo_request_count_unscheduled = obj_mr.search_count(base_domain + [('schedule_date', '=', False)])
