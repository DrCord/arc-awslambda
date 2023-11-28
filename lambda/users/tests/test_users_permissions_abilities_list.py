import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import users_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UsersPermissionsAbilitiesListTestCase(unittest.TestCase):

    def test_permissions_abilities_list_success(self):
        self.assertIsInstance(users_functions.permissions_abilities_list(), list)

    def test_permissions_abilities_list_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.permissions_abilities_list(False)


@arcimoto.runtime.handler
def test_users_permissions_abilities_list():
    return arcimoto.tests.handle_test_result(
        unittest.TextTestRunner().run(
            unittest.TestLoader().loadTestsFromTestCase(UsersPermissionsAbilitiesListTestCase)
        ))


lambda_handler = test_users_permissions_abilities_list
