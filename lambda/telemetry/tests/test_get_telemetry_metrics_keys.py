import logging
import unittest
import uuid

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import telemetry_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GetTelemetryMetricsKeysTestCase(unittest.TestCase):

    def test_get_telemetry_metrics_keys_success_input_version(self):
        self.assertIsInstance(telemetry_functions.get_telemetry_metrics_keys(telemetry_functions.telemetry_get_initial_version()), dict)

    def test_get_telemetry_metrics_keys_success_input_null(self):
        self.assertIsInstance(telemetry_functions.get_telemetry_metrics_keys(), dict)

    # test errors
    def test_get_telemetry_metrics_keys_error_input_invalid_versionId(self):
        with self.assertRaises(ArcimotoNotFoundError):
            telemetry_functions.get_telemetry_metrics_keys(uuid.uuid4().hex)

    def test_get_telemetry_metrics_keys_error_input_invalid_type_versionId(self):
        with self.assertRaises(ArcimotoArgumentError):
            telemetry_functions.get_telemetry_metrics_keys(True)

    def test_get_telemetry_metrics_keys_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            telemetry_functions.get_telemetry_metrics_keys(None, False)


@arcimoto.runtime.handler
def test_get_telemetry_metrics_keys():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(GetTelemetryMetricsKeysTestCase)
    ))


lambda_handler = test_get_telemetry_metrics_keys
