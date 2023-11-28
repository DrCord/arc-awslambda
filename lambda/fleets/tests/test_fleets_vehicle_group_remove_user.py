import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import fleets_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehicleGroupRemoveUserTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.UNITTEST_USERNAME = arcimoto.tests.unit_test_user_get_username()
        cls.vehicle_group_id = fleets_functions.vehicle_group_create()
        fleets_functions.vehicle_group_add_user(cls.vehicle_group_id, cls.UNITTEST_USERNAME)

    @classmethod
    def tearDownClass(cls):
        if cls.vehicle_group_id is not None:
            fleets_functions.vehicle_group_delete(cls.vehicle_group_id)

    def test_vehicle_group_remove_user_success(self):
        response = fleets_functions.vehicle_group_remove_user(self.vehicle_group_id, self.UNITTEST_USERNAME)
        self.assertIsInstance(response, dict)

    # test errors
    def test_vehicle_group_remove_user_error_input_null_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_remove_user(self.vehicle_group_id, None)

    def test_vehicle_group_remove_user_error_input_null_vehicle_group_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_remove_user(None, self.UNITTEST_USERNAME)

    def test_vehicle_group_remove_user_error_input_invalid_type_vehicle_group_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_remove_user('not an integer', self.UNITTEST_USERNAME)

    def test_vehicle_group_remove_user_error_input_invalid_vehicle_group_id_must_be_positive_integer(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_remove_user(-1, self.UNITTEST_USERNAME)

    def test_vehicle_group_remove_user_error_input_invalid_type_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_remove_user(self.vehicle_group_id, 1)

    def test_vehicle_group_remove_user_error_invalid_vehicle_group_to_user_join(self):
        vehicle_groups = fleets_functions.vehicle_groups_list()
        if len(vehicle_groups) > 1:
            non_joined_vehicle_group_id = vehicle_groups[1].get('id', None)
        else:
            non_joined_vehicle_group_id = 2
        with self.assertRaises(ArcimotoNotFoundError):
            fleets_functions.vehicle_group_remove_user(non_joined_vehicle_group_id, self.UNITTEST_USERNAME)

    def test_vehicle_group_remove_user_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            fleets_functions.vehicle_group_remove_user(self.vehicle_group_id, self.UNITTEST_USERNAME, False)


@arcimoto.runtime.handler
def test_vehicle_group_remove_user():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehicleGroupRemoveUserTestCase)
    ))


lambda_handler = test_vehicle_group_remove_user
