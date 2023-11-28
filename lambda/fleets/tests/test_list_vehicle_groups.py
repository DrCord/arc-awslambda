import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehicleGroupsListTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vehicle_groups_initial = fleets_functions.vehicle_groups_list()
        cls.vehicle_groups_initial_length = len(cls.vehicle_groups_initial)
        cls.vehicle_group_id = fleets_functions.vehicle_group_create()

    def test_vehicle_groups_list_success(self):
        vehicle_groups = fleets_functions.vehicle_groups_list()
        vehicle_groups_new_length = len(vehicle_groups)
        self.assertTrue(vehicle_groups_new_length > self.vehicle_groups_initial_length)
        # remove created vehicle_group to test if number of groups is equal to initial
        if self.vehicle_group_id is not None:
            fleets_functions.vehicle_group_delete(self.vehicle_group_id)
        vehicle_groups = fleets_functions.vehicle_groups_list()
        vehicle_groups_final_length = len(vehicle_groups)
        self.assertTrue(vehicle_groups_final_length == self.vehicle_groups_initial_length)

    # test errors
    def test_vehicle_groups_list_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            fleets_functions.vehicle_groups_list(False)


@arcimoto.runtime.handler
def test_vehicle_groups_list():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehicleGroupsListTestCase)
    ))


lambda_handler = test_vehicle_groups_list
