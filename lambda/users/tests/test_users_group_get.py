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


class UsersGroupGetTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.group_id = users_functions.group_create()

    @classmethod
    def tearDownClass(cls):
        users_functions.group_delete(cls.group_id)

    def test_users_group_get_success_group(self):
        self.assertIsInstance(users_functions.group_get(self.group_id), dict)

    # test errors
    def test_users_group_get_error_input_null_group(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.group_get(None)

    def test_users_group_get_error_input_invalid_type_group(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.group_get('not an integer')

    def test_users_group_get_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.group_get(self.group_id, False)


@arcimoto.runtime.handler
def test_users_group_get():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UsersGroupGetTestCase)
    ))


lambda_handler = test_users_group_get
