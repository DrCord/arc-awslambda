import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import telemetry_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GetTelemetryPointsTestCase(unittest.TestCase):

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)
        telemetry_functions.set_telemetry_version(cls.vin, telemetry_functions.telemetry_get_initial_version())
        telemetry_points = {
            "ambient_temp": {},
            "woke_status": {},
            "soc": {},
            "steering_angle": {},
            "odometer": {},
            "speed": {}
        }
        telemetry_functions.set_telemetry_points(cls.vin, telemetry_points)

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_get_telemetry_points_success(self):
        self.assertIsInstance(telemetry_functions.get_telemetry_points(self.vin), dict)

    # test errors
    def test_get_telemetry_points_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            telemetry_functions.get_telemetry_points(None)

    def test_get_telemetry_points_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            telemetry_functions.get_telemetry_points(1)

    def test_get_telemetry_points_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            telemetry_functions.get_telemetry_points(self.vin_invalid)

    def test_get_telemetry_points_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            telemetry_functions.get_telemetry_points(self.vin, False)


@arcimoto.runtime.handler
def test_get_telemetry_points():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(GetTelemetryPointsTestCase)
    ))


lambda_handler = test_get_telemetry_points
