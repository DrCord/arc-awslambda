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


class UsersGroupCreateTestCase(unittest.TestCase):

    def test_users_group_create_success_group(self):
        group_id = users_functions.group_create()
        self.assertIsNotNone(group_id)
        users_functions.group_delete(group_id)

    # test errors
    def test_users_group_create_error_input_null_name(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.group_create({'name': None})

    def test_users_group_create_error_input_invalid_type_name(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.group_create({'name': 1})

    def test_users_group_create_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.group_create(None, False)


@arcimoto.runtime.handler
def test_users_group_create():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UsersGroupCreateTestCase)
    ))


lambda_handler = test_users_group_create
