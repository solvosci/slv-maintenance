# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import fields
from odoo.tests import common


class TestMaintenanceRequestSearchExtra(common.TransactionCase):

    def setUp(self):
        super().setUp()

        self.MaintenanceRequest = self.env["maintenance.request"]

        self.req1 = self.MaintenanceRequest.create({
            'name': 'Request demo 1',
            'stage_id': self.ref('maintenance.stage_0'),
            'maintenance_team_id': self.ref(
                'maintenance.equipment_team_maintenance'),
            'schedule_date': fields.Datetime.now()
        })

    def test_schedule_day(self):
        reqs_no_schedule_date = self.MaintenanceRequest.search(
            [("schedule_date", "=", False)])
        for req in reqs_no_schedule_date:
            self.assertFalse(req.schedule_day)

        reqs_schedule_date = self.MaintenanceRequest.search(
            [("schedule_date", "!=", False)])
        for req in reqs_schedule_date:
            self.assertEqual(req.schedule_day, req.schedule_date.date())
