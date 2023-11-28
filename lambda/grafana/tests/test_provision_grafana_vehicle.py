import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import grafana_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ProvisionGrafanaVehicleTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_provision_grafana_vehicle_success(self):
        self.assertIsInstance(grafana_functions.provision_vehicle(self.vin, True), dict)

    # test errors
    def test_provision_grafana_vehicle_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            grafana_functions.provision_vehicle(None, True)

    def test_provision_grafana_vehicle_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            grafana_functions.provision_vehicle(1, True)

    def test_provision_grafana_vehicle_error_input_invalid_type_show_gps(self):
        with self.assertRaises(ArcimotoArgumentError):
            grafana_functions.provision_vehicle(self.vin, 'not a boolean')

    def test_provision_grafana_vehicle_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            grafana_functions.provision_vehicle(self.vin, True, False)


@arcimoto.runtime.handler
def test_provision_grafana_vehicle():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ProvisionGrafanaVehicleTestCase)
    ))


lambda_handler = test_provision_grafana_vehicle
