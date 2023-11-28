import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import users_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UsersGroupsListTestCase(unittest.TestCase):

    def test_groups_list_success(self):
        self.assertIsInstance(users_functions.groups_list(), list)

    # test errors
    def test_groups_list_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.groups_list(False)


@arcimoto.runtime.handler
def test_users_groups_list():
    return arcimoto.tests.handle_test_result(
        unittest.TextTestRunner().run(
            unittest.TestLoader().loadTestsFromTestCase(UsersGroupsListTestCase)
        ))


lambda_handler = test_users_groups_list
