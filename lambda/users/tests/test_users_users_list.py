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


class UsersUsersListTestCase(unittest.TestCase):

    args = {
        'group_id': None
    }

    def test_users_list_success(self):
        self.assertIsInstance(users_functions.users_list(self.args), list)

    def test_users_list_success_group_id(self):
        args = copy.deepcopy(self.args)
        args['group_id'] = 1
        self.assertIsInstance(users_functions.users_list(args), list)

    def test_users_list_success_group(self):
        args = copy.deepcopy(self.args)
        args['group'] = 1
        del args['group_id']
        self.assertIsInstance(users_functions.users_list(args), list)

    # test errors
    def test_users_users_list_error_input_invalid_type_group_id(self):
        args = copy.deepcopy(self.args)
        args['group_id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.users_list(args)

    def test_users_users_list_error_input_invalid_group_id_must_be_positive_integer(self):
        args = copy.deepcopy(self.args)
        args['group_id'] = -1
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.users_list(args)

    def test_users_list_error_user_unauthorized(self):
        args = copy.deepcopy(self.args)
        args['group_id'] = 1
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.users_list(args, False)


@arcimoto.runtime.handler
def test_users_users_list():
    return arcimoto.tests.handle_test_result(
        unittest.TextTestRunner().run(
            unittest.TestLoader().loadTestsFromTestCase(UsersUsersListTestCase)
        ))


lambda_handler = test_users_users_list
