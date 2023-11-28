import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import telemetry_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SetTelemetryPointsTestCase(unittest.TestCase):

    telemetry_points = {
        "woke_status": {},
        "soc": {},
        "steering_angle": {},
        "odometer": {},
        "speed": {}
    }

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)
        telemetry_functions.set_telemetry_version(cls.vin, telemetry_functions.telemetry_get_initial_version())

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_set_telemetry_points_success(self):
        self.assertIsInstance(telemetry_functions.set_telemetry_points(self.vin, self.telemetry_points), dict)

    # test errors
    def test_set_telemetry_points_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            telemetry_functions.set_telemetry_points(None, self.telemetry_points)

    def test_set_telemetry_points_error_input_null_telemetry_points(self):
        with self.assertRaises(ArcimotoArgumentError):
            telemetry_functions.set_telemetry_points(self.vin, None)

    def test_set_telemetry_points_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            telemetry_functions.set_telemetry_points(1, self.telemetry_points)

    def test_set_telemetry_points_error_input_invalid_type_telemetry_points(self):
        with self.assertRaises(ArcimotoArgumentError):
            telemetry_functions.set_telemetry_points(self.vin, 'not a dictionary')

    def test_set_telemetry_points_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            telemetry_functions.set_telemetry_points(self.vin_invalid, self.telemetry_points)

    def test_set_telemetry_points_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            telemetry_functions.set_telemetry_points(self.vin, self.telemetry_points, False)


@arcimoto.runtime.handler
def test_set_telemetry_points():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(SetTelemetryPointsTestCase)
    ))


lambda_handler = test_set_telemetry_points
