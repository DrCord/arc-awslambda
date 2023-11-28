import logging
import unittest
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehicleGroupTypesListTestCase(unittest.TestCase):

    def test_vehicle_group_types_list_success(self):
        self.assertIsInstance(fleets_functions.vehicle_group_types_list(), dict)

    # test errors
    def test_vehicle_group_types_list_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            fleets_functions.vehicle_group_types_list(False)


@arcimoto.runtime.handler
def test_vehicle_group_types_list():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehicleGroupTypesListTestCase)
    ))


lambda_handler = test_vehicle_group_types_list
