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


class UsersPermissionsAbilityEditTestCase(unittest.TestCase):

    ability = "Unit Test Ability"
    constant = 'UNIT_TEST_EDIT'
    description = "A fake user ability made for a unit test"
    permissions = [{'permission': 'users.abilities.read'}]
    created_id = None

    @classmethod
    def setUpClass(cls):
        created_ability = users_functions.permissions_ability_create(cls.ability, cls.constant, cls.description, cls.permissions)
        cls.created_id = created_ability.get('id')

    @classmethod
    def tearDownClass(cls):
        if cls.created_id is not None:
            try:
                users_functions.permissions_ability_delete(cls.created_id)
            except Exception as e:
                raise ArcimotoException(str(e)) from e

    def test_user_permissions_ability_edit_success(self):
        self.assertIsInstance(users_functions.permissions_ability_edit(self.created_id, self.ability, self.constant, self.description, self.permissions), dict)

    def test_user_permissions_ability_edit_error_null_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_edit(None, self.ability, self.constant, self.description, self.permissions)

    def test_user_permissions_ability_edit_error_null_ability_and_constant_and_description_and_permissions(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_edit(self.created_id, None, None, None, None)

    def test_user_permissions_ability_edit_error_invalid_type_ability(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_edit(self.created_id, 1, self.constant, self.description, self.permissions)

    def test_user_permissions_ability_edit_error_invalid_type_constant(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_edit(self.created_id, self.ability, 1, self.description, self.permissions)

    def test_user_permissions_ability_edit_error_invalid_type_description(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_edit(self.created_id, self.ability, self.constant, 1, self.permissions)

    def test_user_permissions_ability_edit_error_invalid_type_permissions(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_edit(self.created_id, self.ability, self.constant, self.description, 'not a list')

    def test_user_permissions_ability_edit_error_empty_ability(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_edit(self.created_id, '', self.constant, self.description, self.permissions)

    def test_user_permissions_ability_edit_error_empty_constant(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_edit(self.created_id, self.ability, '', self.description, self.permissions)

    def test_user_permissions_ability_edit_error_empty_description(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_edit(self.created_id, self.ability, self.constant, '', self.permissions)

    def test_user_permissions_ability_edit_error_empty_permissions(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.permissions_ability_edit(self.created_id, self.ability, self.constant, self.description, [])

    def test_user_permissions_ability_edit_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.permissions_ability_edit(self.created_id, self.ability, self.constant, self.description, self.permissions, False)


@arcimoto.runtime.handler
def test_users_permissions_ability_edit():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(
            UsersPermissionsAbilityEditTestCase)))


lambda_handler = test_users_permissions_ability_edit
