import logging
import unittest
import uuid

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import arcimoto.db
import users_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UsersAbilityGrantTestCase(unittest.TestCase):

    username = None
    ability_id = 1

    @classmethod
    def setUpClass(cls):
        args = {
            'email': 'unittest+' + uuid.uuid4().hex + '@arcimoto.com',
            'phone': '+15415551212',
            'display_name': 'UnitTest test_users_ability_grant'
        }
        cls.username = users_functions.user_create(args).get('username', None)

    @classmethod
    def tearDownClass(cls):
        if cls.username is not None:
            users_functions.user_delete(cls.username)

    def test_users_ability_grant_success(self):
        self.assertIsInstance(users_functions.ability_grant(self.username, self.ability_id), dict)

    def test_users_ability_grant_error_null_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.ability_grant(None, self.ability_id)

    def test_users_ability_grant_error_null_ability_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.ability_grant(self.username, None)

    def test_users_ability_grant_error_invalid__type_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.ability_grant(1, self.ability_id)

    def test_users_ability_grant_error_invalid_type_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.ability_grant(self.username, 'not an integer')

    def test_users_ability_grant_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.ability_grant(self.username, self.ability_id, False)


@arcimoto.runtime.handler
def test_users_ability_grant():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(
            UsersAbilityGrantTestCase)))


lambda_handler = test_users_ability_grant
