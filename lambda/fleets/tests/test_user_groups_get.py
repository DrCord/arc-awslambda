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


class UserGroupsGetTestCase(unittest.TestCase):

    UNITTEST_REGULAR_USERNAME = None
    vehicle_group_id = None

    @property
    def group_id_invalid(self):
        return fleets_functions.vehicle_groups_list()[-1].get('id', 0) + 1

    @property
    def user_invalid(self):
        return self.UNITTEST_REGULAR_USERNAME + '-' + uuid.uuid4().hex

    @classmethod
    def setUpClass(cls):
        cls.UNITTEST_REGULAR_USERNAME = arcimoto.tests.unit_test_user_get_username()
        cls.vehicle_group_id = fleets_functions.vehicle_group_create()
        fleets_functions.vehicle_group_add_user(cls.vehicle_group_id, cls.UNITTEST_REGULAR_USERNAME)

    @classmethod
    def tearDownClass(cls):
        if cls.vehicle_group_id is not None:
            fleets_functions.vehicle_group_remove_user(cls.vehicle_group_id, cls.UNITTEST_REGULAR_USERNAME)
            fleets_functions.vehicle_group_delete(cls.vehicle_group_id)

    def test_user_groups_get_success(self):
        self.assertIsInstance(fleets_functions.user_groups_get(self.UNITTEST_REGULAR_USERNAME), dict)

    # test errors
    def test_user_groups_get_error_input_null_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.user_groups_get(None)

    def test_user_groups_get_error_user_unauthorized(self):
        UNITTEST_ADMIN_USERNAME = arcimoto.tests.unit_test_user_get_username(True)
        with self.assertRaises(ArcimotoPermissionError):
            fleets_functions.user_groups_get(UNITTEST_ADMIN_USERNAME, False)


@arcimoto.runtime.handler
def test_user_groups_get():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UserGroupsGetTestCase)
    ))


lambda_handler = test_user_groups_get
