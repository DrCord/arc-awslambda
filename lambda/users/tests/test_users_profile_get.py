import logging
import unittest
import uuid

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import users_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UsersProfileGetTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        args = {
            'email': 'unittest' + uuid.uuid4().hex + '@arcimoto.com',
            'phone': '+15415551212',
            'display_name': 'Unit Test User'
        }

        cls.UNITTEST_USER = arcimoto.tests.unit_test_user_get_username()
        cls.username = users_functions.user_create(args).get('username', None)

    @classmethod
    def tearDownClass(cls):
        users_functions.user_delete(cls.username)

    def test_users_profile_get_success(self):
        self.assertIsInstance(users_functions.profile_get(self.username), dict)

    def test_users_profile_get_success_get_own_user(self):
        self.assertIsInstance(users_functions.profile_get(self.UNITTEST_USER, False), dict)

    # test errors
    def test_users_profile_get_error_input_null_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_get(None)

    def test_users_profile_get_error_input_invalid_type_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_get(1)

    def test_users_profile_get_error_input_invalid_format_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_get('not a UUID')

    def test_users_profile_get_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.profile_get(self.username, False)


@arcimoto.runtime.handler
def test_users_profile_get():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UsersProfileGetTestCase)
    ))


lambda_handler = test_users_profile_get
