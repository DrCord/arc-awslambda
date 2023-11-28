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


class UsersPermissionsAbilityCreateTestCase(unittest.TestCase):

    ability = 'Unit Test Ability'
    constant = 'UNIT_TEST_CREATE'
    description = 'A fake user ability made for a unit test'
    permissions = [{'permission': 'users.abilities.read'}]
    created_id = None

    def test_user_permissions_ability_create_success(self):
        created_ability = users_functions.permissions_ability_create(self.ability, self.constant, self.description, self.permissions)
        self.created_id = created_ability.get('id')
        self.assertIsInstance(created_ability, dict)
        # Reverse any created records.
        # This would normally be done in a tearDownClass method.
        # However the class method does not have access to the self instance, only the cls
        if self.created_id is not None:
            try:
                users_functions.permissions_ability_delete(self.created_id)
            except Exception as e:
                raise ArcimotoException(str(e)) from e

    def test_user_permissions_ability_create_error_null_ability(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_create(None, self.constant, self.description, self.permissions)

    def test_user_permissions_ability_create_error_null_constant(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_create(self.ability, None, self.description, self.permissions)

    def test_user_permissions_ability_create_error_null_description(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_create(self.ability, self.constant, None, self.permissions)

    def test_user_permissions_ability_create_error_null_permissions(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_create(self.ability, self.constant, self.description, None)

    def test_user_permissions_ability_create_error_invalid_type_ability(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_create(1, self.constant, self.description, self.permissions)

    def test_user_permissions_ability_create_error_invalid_type_constant(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_create(self.ability, 1, self.description, self.permissions)

    def test_user_permissions_ability_create_error_invalid_type_description(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_create(self.ability, self.constant, 1, self.permissions)

    def test_user_permissions_ability_create_error_invalid_type_permissions(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_create(self.ability, self.constant, self.description, 'not a list')

    def test_user_permissions_ability_create_error_empty_ability(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_create('', self.constant, self.description, self.permissions)

    def test_user_permissions_ability_create_error_empty_constant(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_create(self.ability, '', self.description, self.permissions)

    def test_user_permissions_ability_create_error_empty_description(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_create(self.ability, self.constant, '', self.permissions)

    def test_user_permissions_ability_create_error_empty_permissions(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_create(self.ability, self.constant, self.description, [])

    def test_user_permissions_ability_create_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.permissions_ability_create(self.ability, self.constant, self.description, self.permissions, False)


@arcimoto.runtime.handler
def test_users_permissions_ability_create():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(
            UsersPermissionsAbilityCreateTestCase)))


lambda_handler = test_users_permissions_ability_create
