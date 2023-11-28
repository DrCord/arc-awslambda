import logging
import unittest
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import users_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UsersAddPermissionToGroupTestCase(unittest.TestCase):

    args = {
        'permission': 'users.group.add-permission',
        'resource': None,
        'group': None,
        'group_id': None
    }

    @classmethod
    def setUpClass(cls):
        cls.group_id = users_functions.group_create()
        cls.args['group'] = cls.group_id

    @classmethod
    def tearDownClass(cls):
        users_functions.group_delete(cls.group_id)

    def test_users_add_permission_to_group_success_group(self):
        self.assertIsInstance(users_functions.add_permission_to_group(self.args), dict)
        users_functions.remove_permission_from_group(self.args)

    def test_users_add_permission_to_group_success_group_id(self):
        args = copy.deepcopy(self.args)
        del args['group']
        args['group_id'] = self.group_id
        self.assertIsInstance(users_functions.add_permission_to_group(args), dict)
        users_functions.remove_permission_from_group(self.args)

    # test errors
    def test_users_add_permission_to_group_error_input_null_permission(self):
        args = copy.deepcopy(self.args)
        args['permission'] = None
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.add_permission_to_group(args)

    def test_users_add_permission_to_group_error_input_null_group(self):
        args = copy.deepcopy(self.args)
        args['group'] = None
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.add_permission_to_group(args)

    def test_users_add_permission_to_group_error_input_null_group_id(self):
        args = copy.deepcopy(self.args)
        args['group'] = None
        args['group_id'] = None
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.add_permission_to_group(args)

    def test_users_add_permission_to_group_error_input_invalid_type_permission(self):
        args = copy.deepcopy(self.args)
        args['permission'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.add_permission_to_group(args)

    def test_users_add_permission_to_group_error_input_invalid_type_resource(self):
        args = copy.deepcopy(self.args)
        args['resource'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.add_permission_to_group(args)

    def test_users_add_permission_to_group_error_input_invalid_type_group(self):
        args = copy.deepcopy(self.args)
        args['group'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.add_permission_to_group(args)

    def test_users_add_permission_to_group_error_input_invalid_type_group_id(self):
        args = copy.deepcopy(self.args)
        args['group'] = None
        args['group_id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.add_permission_to_group(args)

    def test_users_add_permission_to_group_error_input_invalid_group_id_must_be_positive_integer(self):
        args = copy.deepcopy(self.args)
        args['group'] = None
        args['group_id'] = -1
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.add_permission_to_group(args)

    def test_users_add_permission_to_group_error_user_unauthorized(self):
        args = copy.deepcopy(self.args)
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.add_permission_to_group(args, False)


@arcimoto.runtime.handler
def test_users_add_permission_to_group():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UsersAddPermissionToGroupTestCase)
    ))


lambda_handler = test_users_add_permission_to_group
