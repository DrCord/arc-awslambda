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


class UsersRemoveUserFromGroupTestCase(unittest.TestCase):

    args = {
        'username': None,
        'group': None,
        'group_id': None
    }

    @classmethod
    def setUpClass(cls):
        args = {
            'email': 'unittest' + uuid.uuid4().hex + '@arcimoto.com',
            'phone': '+15415551212',
            'display_name': 'Unit Test User'
        }
        cls.username = users_functions.user_create(args).get('username', None)
        cls.args['username'] = cls.username
        cls.group_id = users_functions.group_create()
        cls.args['group'] = cls.group_id

    @classmethod
    def tearDownClass(cls):
        users_functions.group_delete(cls.group_id)
        users_functions.user_delete(cls.username)

    def test_users_remove_user_from_group_success_group(self):
        users_functions.add_user_to_group(self.args)
        self.assertIsInstance(users_functions.remove_user_from_group(self.args), dict)

    def test_users_remove_user_from_group_success_group_id(self):
        args = copy.deepcopy(self.args)
        del args['group']
        args['group_id'] = self.group_id
        users_functions.add_user_to_group(args)
        self.assertIsInstance(users_functions.remove_user_from_group(self.args), dict)

    # test errors
    def test_users_remove_user_from_group_error_input_null_username(self):
        args = copy.deepcopy(self.args)
        args['username'] = None
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.remove_user_from_group(args)

    def test_users_remove_user_from_group_error_input_null_group(self):
        args = copy.deepcopy(self.args)
        args['group'] = None
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.remove_user_from_group(args)

    def test_users_remove_user_from_group_error_input_null_group_id(self):
        args = copy.deepcopy(self.args)
        args['group'] = None
        args['group_id'] = None
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.remove_user_from_group(args)

    def test_users_remove_user_from_group_error_input_invalid_type_username(self):
        args = copy.deepcopy(self.args)
        args['username'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.remove_user_from_group(args)

    def test_users_remove_user_from_group_error_input_invalid_type_group(self):
        args = copy.deepcopy(self.args)
        args['group'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.remove_user_from_group(args)

    def test_users_remove_user_from_group_error_input_invalid_type_group_id(self):
        args = copy.deepcopy(self.args)
        args['group'] = None
        args['group_id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.remove_user_from_group(args)

    def test_users_remove_user_from_group_error_input_invalid_group_id_must_be_positive_integer(self):
        args = copy.deepcopy(self.args)
        args['group'] = -1
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.remove_user_from_group(args)
        args['group'] = None
        args['group_id'] = -1
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.remove_user_from_group(args)

    def test_users_remove_user_from_group_error_input_invalid_format_username(self):
        args = copy.deepcopy(self.args)
        args['username'] = 'not a UUID'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.remove_user_from_group(args)

    def test_users_remove_user_from_group_error_user_unauthorized(self):
        args = copy.deepcopy(self.args)
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.remove_user_from_group(args, False)


@arcimoto.runtime.handler
def test_users_remove_user_from_group():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UsersRemoveUserFromGroupTestCase)
    ))


lambda_handler = test_users_remove_user_from_group
