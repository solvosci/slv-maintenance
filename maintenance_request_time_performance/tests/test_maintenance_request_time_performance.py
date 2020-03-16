# Copyright 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import odoo.tests.common as test_common
from odoo import fields
from odoo.exceptions import ValidationError
from datetime import timedelta


class TestMaintenanceRequestTimePerformance(test_common.TransactionCase):

    def setUp(self):
        super().setUp()

        MaintenanceStage = self.env['maintenance.stage']
        self.stage_inprogress = MaintenanceStage.create({
            'name': 'my in progress stage',
            'in_progress': True})
        self.stage_done = MaintenanceStage.create({
            'name': 'my done stage',
            'done': True})

        MaintenanceRequest = self.env['maintenance.request']
        self.request1 = MaintenanceRequest.create({
            'name': 'My corrective request',
            'user_id': self.env.ref('base.user_admin').id,
            'schedule_date': fields.Datetime.now(),
            'duration': 1.0,
            'maintenance_type': 'corrective'})

        self.request2 = MaintenanceRequest.create({
            'name': 'My preventive request',
            'user_id': self.env.ref('base.user_admin').id,
            'schedule_date': fields.Date.today(),
            'duration': 2.0,
            'maintenance_type': 'preventive'})

    def test_01_stage(self):
        with self.assertRaises(ValidationError):
            self.stage_inprogress.done = True

    def test_02_request(self):
        self.assertFalse(self.request1.start_request_datetime)
        self.assertFalse(self.request1.start_request_date)
        self.assertFalse(self.request1.end_request_datetime)
        self.assertFalse(self.request1.end_request_date)
        self.assertFalse(self.request1.start_request_datetime_required)
        self.assertFalse(self.request1.end_request_datetime_required)

        self.request1.stage_id = self.stage_inprogress

        self.assertTrue(self.request1.start_request_datetime_required)
        self.assertFalse(self.request1.end_request_datetime_required)
        self.assertTrue(self.request1.start_request_datetime)
        self.assertEqual(self.request1.start_request_datetime.date(),
                         self.request1.start_request_date)

        self.request1.start_request_datetime -= timedelta(hours=1)
        self.request1.stage_id = self.stage_done

        self.assertTrue(self.request1.start_request_datetime_required)
        self.assertTrue(self.request1.end_request_datetime_required)
        self.assertTrue(self.request1.end_request_datetime)
        self.assertEqual(self.request1.end_request_datetime.date(),
                         self.request1.end_request_date)
        real_duration = (
            self.request1.end_request_datetime -
            self.request1.start_request_datetime).total_seconds() / 3600
        self.assertEqual(round(self.request1.real_request_duration, 2),
                         round(real_duration, 2))
        self.assertEqual(round(self.request1.duration_difference, 2),
                         round(real_duration - self.request1.duration, 2))
        completion_delay = (
                self.request1.end_request_datetime -
                (self.request1.schedule_date +
                 timedelta(hours=self.request1.duration))
        ).total_seconds() / 3600
        self.assertEqual(round(self.request1.completion_delay, 2),
                         round(completion_delay, 2))

        self.request2.stage_id = self.stage_inprogress

        with self.assertRaises(ValidationError):
            self.request2.end_request_datetime = (
                self.request2.start_request_datetime - timedelta(hours=1))
        end_request_datetime = self.request2.start_request_datetime
        real_duration = 1.5
        completion_delay = real_duration - self.request2.duration
        self.request2.start_request_datetime = \
            end_request_datetime - timedelta(hours=real_duration)
        self.request2.end_request_datetime = end_request_datetime

        self.request2.stage_id = self.stage_done

        self.assertEqual(round(self.request2.real_request_duration, 2),
                         round(real_duration, 2))
        self.assertEqual(round(self.request2.completion_delay, 2),
                         round(completion_delay, 2))
