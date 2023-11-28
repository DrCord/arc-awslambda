import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehiclesFirmwareComponentsListTestCase(unittest.TestCase):

    def test_vehicles_firmware_components_list_success(self):
        self.assertIsInstance(vehicles_functions.firmware_components_list(), dict)

    # test errors
    def test_vehicles_firmware_components_list_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.firmware_components_list(False)


@arcimoto.runtime.handler
def test_vehicles_firmware_components_list():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehiclesFirmwareComponentsListTestCase)
    ))


lambda_handler = test_vehicles_firmware_components_list
