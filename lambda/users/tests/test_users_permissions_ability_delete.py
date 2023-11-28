import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import arcimoto.db
import users_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UsersPermissionsAbilityDeleteTestCase(unittest.TestCase):

    ability = 'Unit Test Ability'
    constant = 'UNIT_TEST_DELETE'
    description = 'A fake user ability made for a unit test'
    permissions = [{'permission': 'users.abilities.read'}]
    created_id = None

    @classmethod
    def setUpClass(cls):
        created_ability = users_functions.permissions_ability_create(cls.ability, cls.constant, cls.description, cls.permissions)
        cls.created_id = created_ability.get('id')

    def test_user_permissions_ability_delete_success(self):
        self.assertIsInstance(users_functions.permissions_ability_delete(self.created_id), dict)

    def test_user_permissions_ability_delete_error_null_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_delete(None)

    def test_user_permissions_ability_delete_error_invalid_type_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_delete('not an integer')

    def test_user_permissions_ability_delete_error_invalid_min_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_delete(-1)

    def test_user_permissions_ability_delete_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.permissions_ability_delete(self.created_id, False)


@arcimoto.runtime.handler
def test_users_permissions_ability_delete():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(
            UsersPermissionsAbilityDeleteTestCase)))


lambda_handler = test_users_permissions_ability_delete
