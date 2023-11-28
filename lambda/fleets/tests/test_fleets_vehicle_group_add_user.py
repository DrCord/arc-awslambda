import logging
import unittest
import uuid

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehicleGroupAddUserTestCase(unittest.TestCase):

    @property
    def group_id_invalid(self):
        return fleets_functions.vehicle_groups_list()[-1].get('id', 0) + 1

    @property
    def user_invalid(self):
        return self.UNITTEST_USERNAME + '-' + uuid.uuid4().hex

    @classmethod
    def setUpClass(cls):
        cls.UNITTEST_USERNAME = arcimoto.tests.unit_test_user_get_username()
        cls.vehicle_group_id = fleets_functions.vehicle_group_create()

    @classmethod
    def tearDownClass(cls):
        fleets_functions.vehicle_group_remove_user(cls.vehicle_group_id, cls.UNITTEST_USERNAME)
        if cls.vehicle_group_id is not None:
            fleets_functions.vehicle_group_delete(cls.vehicle_group_id)

    def test_vehicle_group_add_user_success(self):
        response = fleets_functions.vehicle_group_add_user(self.vehicle_group_id, self.UNITTEST_USERNAME)
        self.assertIsInstance(response, dict)

    # test errors
    def test_vehicle_group_add_user_error_input_null_group(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_add_user(None, self.UNITTEST_USERNAME)

    def test_vehicle_group_add_user_error_input_null_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_add_user(self.vehicle_group_id, None)

    def test_vehicle_group_add_user_error_input_invalid_type_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_add_user(self.vehicle_group_id, 1)

    def test_vehicle_group_add_user_error_input_invalid_type_vehicle_group_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_add_user('not an integer', self.UNITTEST_USERNAME)

    def test_vehicle_group_add_user_error_input_invalid_vehicle_group_id_must_be_positive_integer(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_add_user(-1, self.UNITTEST_USERNAME)

    def test_vehicle_group_add_user_error_invalid_group(self):
        with self.assertRaises(ArcimotoNotFoundError):
            fleets_functions.vehicle_group_add_user(self.group_id_invalid, self.UNITTEST_USERNAME)

    def test_vehicle_group_add_user_error_invalid_user(self):
        with self.assertRaises(ArcimotoNotFoundError):
            fleets_functions.vehicle_group_add_user(self.vehicle_group_id, self.user_invalid)

    def test_vehicle_group_add_user_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            fleets_functions.vehicle_group_add_user(self.vehicle_group_id, self.UNITTEST_USERNAME, False)


@arcimoto.runtime.handler
def test_vehicle_group_add_user():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehicleGroupAddUserTestCase)
    ))


lambda_handler = test_vehicle_group_add_user
