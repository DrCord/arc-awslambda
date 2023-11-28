import logging
import unittest
import copy
import uuid

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import users_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UsersAddPreferenceToUserTestCase(unittest.TestCase):

    args = {
        'username': None,
        'preference_identifier': 'dark_mode',
        'preference_value': '1'
    }

    @classmethod
    def setUpClass(cls):
        args = {
            'email': 'unittest+' + uuid.uuid4().hex + '@arcimoto.com',
            'phone': '+15415551212',
            'display_name': 'Unit Test User'
        }
        cls.username = users_functions.user_create(args).get('username', None)
        cls.args['username'] = cls.username

    @classmethod
    def tearDownClass(cls):
        users_functions.user_delete(cls.username)

    def test_users_add_preference_to_user_success(self):
        self.assertIsInstance(users_functions.add_preference_to_user(self.args), dict)

    # test errors
    def test_users_add_preference_to_user_error_input_null_username(self):
        args = copy.deepcopy(self.args)
        args['username'] = None
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.add_preference_to_user(args)

    def test_users_add_preference_to_user_error_input_invalid_type_username(self):
        args = copy.deepcopy(self.args)
        args['username'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.add_preference_to_user(args)

    def test_users_add_preference_to_user_error_input_invalid_format_username(self):
        args = copy.deepcopy(self.args)
        args['username'] = 'not a UUID'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.add_preference_to_user(args)

    def test_users_add_preference_to_user_error_user_unauthorized(self):
        args = copy.deepcopy(self.args)
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.add_preference_to_user(args, False)

    def test_users_add_preference_to_user_error_input_null_preference_identifier(self):
        args = copy.deepcopy(self.args)
        args['preference_identifier'] = None
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.add_preference_to_user(args)

    def test_users_add_preference_to_user_error_input_invalid_type_preference_identifier(self):
        args = copy.deepcopy(self.args)
        args['preference_identifier'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.add_preference_to_user(args)

    def test_users_add_preference_to_user_error_input_null_preference_value(self):
        args = copy.deepcopy(self.args)
        args['preference_identifier'] = None
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.add_preference_to_user(args)

    def test_users_add_preference_to_user_error_input_invalid_type_preference_value(self):
        args = copy.deepcopy(self.args)
        args['preference_value'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.add_preference_to_user(args)


@arcimoto.runtime.handler
def test_users_add_preference_to_user():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UsersAddPreferenceToUserTestCase)
    ))


lambda_handler = test_users_add_preference_to_user
