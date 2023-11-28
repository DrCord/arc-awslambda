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


class UsersGroupDeleteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.group_id = users_functions.group_create()

    def test_users_group_delete_success_group(self):
        self.assertIsInstance(users_functions.group_delete(self.group_id), dict)

    # test errors
    def test_users_group_delete_error_input_null_group(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.group_delete(None)

    def test_users_group_delete_error_input_invalid_type_group(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.group_delete('not an integer')

    def test_users_group_delete_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.group_delete(self.group_id, False)


@arcimoto.runtime.handler
def test_users_group_delete():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UsersGroupDeleteTestCase)
    ))


lambda_handler = test_users_group_delete
