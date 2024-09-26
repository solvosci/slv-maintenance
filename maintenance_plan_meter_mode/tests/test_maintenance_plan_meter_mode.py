# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

import odoo.tests.common as test_common
from odoo import fields, _
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class TestMaintenancePlanMeterMode(test_common.TransactionCase):

    def setUp(self):
        super().setUp()

        self.maintenance_request_obj = self.env["maintenance.request"]
        self.maintenance_kind_obj = self.env["maintenance.kind"]
        self.maintenance_equipment_obj = self.env["maintenance.equipment"]
        self.maintenance_plan_obj = self.env["maintenance.plan"]
        self.cron = self.env.ref('maintenance.maintenance_requests_cron')
        self.today_date = fields.Date.today()

        self.meter_mode_kind_auto = self.maintenance_kind_obj.create({
            "name": "Every X usages plan kind",
            "active": True,
        })
        self.meter_mode_kind_external = self.maintenance_kind_obj.create({
            "name": "External incremented plan kind",
            "active": True,
        })

        self.equipment_1 = self.maintenance_equipment_obj.create({
            "name": "A machine that needs revision every X usages",
        })
        self.maintenance_plan_1 = self.maintenance_plan_obj.create({
            "name": "Every 1,000 usages",
            "equipment_id": self.equipment_1.id,
            "maintenance_kind_id": self.meter_mode_kind_auto.id,
            "meter_mode": True,
            "meter_autoinc_mode": True,
            "meter_autoinc_value": 50,
            "meter_autoinc_unit": self.env.ref("uom.product_uom_unit").id,
            "meter_autoinc_maxvalue": 1000,
            "start_maintenance_date": self.today_date - timedelta(days=1)
        })

        self.equipment_2 = self.maintenance_equipment_obj.create({
            "name": "A machine that has a meter externally incremented",
        })
        self.maintenance_plan_2 = self.maintenance_plan_obj.create({
            "name": "When meter increases 2,000",
            "equipment_id": self.equipment_2.id,
            "maintenance_kind_id": self.meter_mode_kind_external.id,
            "meter_mode": True,
            "meter_autoinc_mode": False,
            "meter_autoinc_maxvalue": 2000,
            "start_maintenance_date": self.today_date - timedelta(days=1)
        })

    def test_meter_mode(self):
        my_domain_1 = \
            [('maintenance_plan_id', '=', self.maintenance_plan_1.id)]
        my_domain_2 = \
            [('maintenance_plan_id', '=', self.maintenance_plan_2.id)]

        # As first cron execution, only meter_autoinc_lastupdate will be 
        #  updated for both plans
        meter_initial_value_1 = 975
        meter_initial_value_2 = 1975
        self.maintenance_plan_1.meter_current_value = meter_initial_value_1
        self.maintenance_plan_2.meter_current_value = meter_initial_value_2
        self.cron.method_direct_trigger()
        generated_requests_1 = \
            self.maintenance_request_obj.search(my_domain_1)
        generated_requests_2 = \
            self.maintenance_request_obj.search(my_domain_2)
        self.assertEqual(len(generated_requests_1), 0)
        self.assertEqual(len(generated_requests_2), 0)
        self.assertEqual(
            self.maintenance_plan_1.meter_current_value,
            meter_initial_value_1)
        self.assertEqual(
            self.maintenance_plan_2.meter_current_value,
            meter_initial_value_2)
        self.assertEqual(
            self.maintenance_plan_1.meter_autoinc_lastupdate,
            self.today_date)
        self.assertEqual(
            self.maintenance_plan_2.meter_autoinc_lastupdate,
            self.today_date)

        # With "second" cron execution, only auto incremental plan will 
        #  generate a request 
        self.maintenance_plan_1.meter_autoinc_lastupdate -= timedelta(days=1)
        self.maintenance_plan_2.meter_autoinc_lastupdate -= timedelta(days=1)
        self.cron.method_direct_trigger()
        generated_requests_1 = \
            self.maintenance_request_obj.search(my_domain_1)
        generated_requests_2 = \
            self.maintenance_request_obj.search(my_domain_2)
        self.assertEqual(len(generated_requests_1), 1)
        self.assertEqual(len(generated_requests_2), 0)
        self.assertEqual(
            self.maintenance_plan_1.meter_current_value,
            meter_initial_value_1 + 
                self.maintenance_plan_1.meter_autoinc_value)
        self.assertEqual(
            self.maintenance_plan_1.meter_autoinc_lastvalue,
            self.maintenance_plan_1.meter_current_value)
        self.assertEqual(
            self.maintenance_plan_2.meter_current_value,
            meter_initial_value_2)
        self.assertEqual(
            self.maintenance_plan_2.meter_autoinc_lastupdate,
            self.today_date)

        # With "third" cron execution before a manual update, manual plan will
        #  generate a request
        self.maintenance_plan_2.meter_autoinc_lastupdate -= timedelta(days=1)
        self.maintenance_plan_2.meter_current_value += 50
        self.cron.method_direct_trigger()
        generated_requests_2 = \
            self.maintenance_request_obj.search(my_domain_2)
        self.assertEqual(len(generated_requests_2), 1)
        self.assertEqual(
            self.maintenance_plan_2.meter_autoinc_lastvalue,
            self.maintenance_plan_2.meter_current_value)
