import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import telemetry_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TelemetryPointsGetDefaultsTestCase(unittest.TestCase):

    def test_telemetry_points_get_defaults_success(self):
        self.assertIsInstance(telemetry_functions.telemetry_points_get_defaults(), dict)

    # test errors
    def test_telemetry_points_get_defaults_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            telemetry_functions.telemetry_points_get_defaults(False)


@arcimoto.runtime.handler
def test_telemetry_points_get_defaults():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(TelemetryPointsGetDefaultsTestCase)
    ))


lambda_handler = test_telemetry_points_get_defaults
