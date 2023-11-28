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


class UsersDisableUserTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        args = {
            'email': 'unittest' + uuid.uuid4().hex + '@arcimoto.com',
            'phone': '+15415551212',
            'display_name': 'Unit Test User'
        }
        cls.username = users_functions.user_create(args).get('username', None)

    @classmethod
    def tearDownClass(cls):
        users_functions.user_delete(cls.username)

    def test_users_disable_user_success(self):
        self.assertIsInstance(users_functions.user_disable(self.username), dict)

    # test errors
    def test_users_disable_user_error_input_null_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_disable(None)

    def test_users_disable_user_error_input_invalid_type_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_disable(1)

    def test_users_disable_user_error_input_invalid_format_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_disable('not a username UUID')

    def test_users_disable_user_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.user_disable(self.username, False)


@arcimoto.runtime.handler
def test_users_disable_user():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UsersDisableUserTestCase)
    ))


lambda_handler = test_users_disable_user
