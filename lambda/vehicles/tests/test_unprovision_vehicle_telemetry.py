import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UnprovisionVehicleTelemetryTestCase(unittest.TestCase):

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)

    def test_unprovision_vehicle_telemetry_success(self):
        self.assertIsInstance(vehicles_functions.unprovision_vehicle_telemetry(self.vin), dict)

    # test errors
    def test_unprovision_vehicle_telemetry_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.unprovision_vehicle_telemetry(None)

    def test_unprovision_vehicle_telemetry_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            vehicles_functions.unprovision_vehicle_telemetry(self.vin_invalid)

    def test_unprovision_vehicle_telemetry_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.unprovision_vehicle_telemetry(1)

    def test_unprovision_vehicle_telemetry_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.unprovision_vehicle_telemetry(self.vin, False)


@arcimoto.runtime.handler
def test_unprovision_vehicle_telemetry():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UnprovisionVehicleTelemetryTestCase)
    ))


lambda_handler = test_unprovision_vehicle_telemetry
