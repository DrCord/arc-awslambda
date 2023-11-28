import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import users_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UsersPreferencesListTestCase(unittest.TestCase):

    def test_preferences_list_success(self):
        self.assertIsInstance(users_functions.preferences_list(), list)


@arcimoto.runtime.handler
def test_users_preferences_list():
    return arcimoto.tests.handle_test_result(
        unittest.TextTestRunner().run(
            unittest.TestLoader().loadTestsFromTestCase(UsersPreferencesListTestCase)
        ))


lambda_handler = test_users_preferences_list
