import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import managed_session_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ManagedSessionTelemetryGetTestCase(unittest.TestCase):

    managed_session_id = 4

    @property
    def managed_session_id_invalid(self):
        return managed_session_functions.managed_sessions_get_highest_id() + 1

    def test_managed_session_telemetry_get_success(self):
        self.assertIsInstance(managed_session_functions.telemetry_get(self.managed_session_id), dict)

    # test errors
    def test_managed_session_telemetry_get_error_input_null_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            managed_session_functions.telemetry_get(None)

    def test_managed_session_telemetry_get_error_input_invalid_type_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            managed_session_functions.telemetry_get('not an integer id', None)

    def test_managed_session_telemetry_get_error_input_invalid_id_min(self):
        with self.assertRaises(ArcimotoArgumentError):
            managed_session_functions.telemetry_get(-1)

    def test_managed_session_telemetry_get_error_input_invalid_id(self):
        with self.assertRaises(ArcimotoException):
            managed_session_functions.telemetry_get(self.managed_session_id_invalid)

    def test_managed_session_telemetry_get_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            managed_session_functions.telemetry_get(self.managed_session_id, False)


@arcimoto.runtime.handler
def test_managed_session_telemetry_get():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ManagedSessionTelemetryGetTestCase)
    ))


lambda_handler = test_managed_session_telemetry_get
