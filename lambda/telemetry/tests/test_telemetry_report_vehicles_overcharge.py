import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import telemetry_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TelemetryReportVehiclesOverchargeTestCase(unittest.TestCase):

    def test_telemetry_report_vehicles_overcharge_success(self):
        self.assertIsInstance(telemetry_functions.telemetry_report_vehicles_overcharge(), dict)


@arcimoto.runtime.handler
def test_telemetry_report_vehicles_overcharge():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(TelemetryReportVehiclesOverchargeTestCase)
    ))


lambda_handler = test_telemetry_report_vehicles_overcharge
