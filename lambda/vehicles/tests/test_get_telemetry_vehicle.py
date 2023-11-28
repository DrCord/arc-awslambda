import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GetTelemetryVehicleTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_get_telemetry_vehicle_success(self):
        self.assertIsInstance(vehicles_functions.get_telemetry_vehicle(self.vin), dict)

    # test errors
    def test_get_telemetry_vehicle_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.get_telemetry_vehicle(None)

    def test_get_telemetry_vehicle_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.get_telemetry_vehicle(1)

    def test_get_telemetry_vehicle_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.get_telemetry_vehicle(self.vin, False)


@arcimoto.runtime.handler
def test_get_telemetry_vehicle():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(GetTelemetryVehicleTestCase)
    ))


lambda_handler = test_get_telemetry_vehicle
