import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import telemetry_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SetTelemetryVersionTestCase(unittest.TestCase):

    @property
    def TELEMETRY_VERSION_INITIAL(self):
        return telemetry_functions.telemetry_get_initial_version()

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_set_telemetry_version_success(self):
        self.assertIsInstance(telemetry_functions.set_telemetry_version(self.vin, self.TELEMETRY_VERSION_INITIAL), dict)

    # test errors
    def test_set_telemetry_version_error_input_null_vin(self):
        with self.assertRaises(Exception):
            telemetry_functions.set_telemetry_version(None, self.TELEMETRY_VERSION_INITIAL)

    def test_set_telemetry_version_error_input_null_version(self):
        with self.assertRaises(Exception):
            telemetry_functions.set_telemetry_version(self.vin, None)

    def test_set_telemetry_version_error_input_invalid_type_vin(self):
        with self.assertRaises(Exception):
            telemetry_functions.set_telemetry_version(1, self.TELEMETRY_VERSION_INITIAL)

    def test_set_telemetry_version_error_input_invalid_type_version(self):
        with self.assertRaises(Exception):
            telemetry_functions.set_telemetry_version(self.vin, 1)

    def test_set_telemetry_version_error_input_invalid_vin(self):
        with self.assertRaises(Exception):
            telemetry_functions.set_telemetry_version(self.vin_invalid, self.TELEMETRY_VERSION_INITIAL)

    def test_set_telemetry_version_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            telemetry_functions.set_telemetry_version(self.vin, self.TELEMETRY_VERSION_INITIAL, False)


@arcimoto.runtime.handler
def test_set_telemetry_version():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(SetTelemetryVersionTestCase)
    ))


lambda_handler = test_set_telemetry_version
