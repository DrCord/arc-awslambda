import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ProvisionVehicleTelemetryTestCase(unittest.TestCase):

    MODEL_RELEASE_ID = 1

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()

    def test_provision_vehicle_telemetry_success(self):
        self.assertIsInstance(vehicles_functions.provision_vehicle_telemetry(self.vin, self.MODEL_RELEASE_ID), dict)
        vehicles_functions.unprovision_vehicle_telemetry(self.vin)

    # test errors
    def test_provision_vehicle_telemetry_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.provision_vehicle_telemetry(None, self.MODEL_RELEASE_ID)

    def test_provision_vehicle_telemetry_error_input_null_model_release_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.provision_vehicle_telemetry(self.vin, None)

    def test_provision_vehicle_telemetry_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.provision_vehicle_telemetry(1, self.MODEL_RELEASE_ID)

    def test_provision_vehicle_telemetry_error_input_invalid_type_model_release_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.provision_vehicle_telemetry(self.vin, 'not an integer')

    def test_provision_vehicle_telemetry_error_input_invalid_model_release_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.provision_vehicle_telemetry(self.vin, 0)

    def test_provision_vehicle_telemetry_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.provision_vehicle_telemetry(self.vin, self.MODEL_RELEASE_ID, False)


@arcimoto.runtime.handler
def test_provision_vehicle_telemetry():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ProvisionVehicleTelemetryTestCase)
    ))


lambda_handler = test_provision_vehicle_telemetry
