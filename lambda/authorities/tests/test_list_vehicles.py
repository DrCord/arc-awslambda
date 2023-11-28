import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import authorities_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ListVehiclesTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        # this cannot be cleaned up, the arcimoto authority cannot be removed from a vehicle
        authorities_functions.provision_vehicle_authority(authorities_functions.ARCIMOTO_AUTHORITY_ID, cls.vin)

    def test_list_vehicles_success_no_input(self):
        self.assertIsInstance(authorities_functions.list_vehicles(), list)

    def test_list_vehicles_success_filter_args_vin(self):
        self.assertTrue(len(authorities_functions.list_vehicles({'vin': self.vin})) >= 1)

    # test errors
    def test_list_vehicles_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            authorities_functions.list_vehicles(None, False)


@arcimoto.runtime.handler
def test_list_vehicles():
    return arcimoto.tests.handle_test_result(
        unittest.TextTestRunner().run(
            unittest.TestLoader().loadTestsFromTestCase(ListVehiclesTestCase)
        ))


lambda_handler = test_list_vehicles
