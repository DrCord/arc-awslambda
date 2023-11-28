import logging
import unittest
import uuid

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import users_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UsersUserMfaTotpEnableTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        uuid_hex = uuid.uuid4().hex
        args = {
            'email': f'unittest+{uuid_hex}@arcimoto.com',
            'phone': '+15415551212',
            'display_name': f'Unit Test Created User: {uuid_hex}'
        }

        cls.UNITTEST_USER = arcimoto.tests.unit_test_user_get_username()
        cls.username = users_functions.user_create(args).get('username', None)

    @classmethod
    def tearDownClass(cls):
        # Unable to pass, needs to run after TOTP token association and verification
        # users_functions.user_mfa_totp_disable(cls.UNITTEST_USER)
        users_functions.user_delete(cls.username)

    # disabled to potentially enable later, but cannot pass as needs to run after totp token association and verification
    # def test_users_user_mfa_totp_enable_success(self):
    #     self.assertIsInstance(users_functions.user_mfa_totp_enable(self.username), dict)

    # disabled to potentially enable later, but cannot pass as needs to run after totp token association and verification
    # def test_users_user_mfa_totp_enable_success_own_user(self):
    #     self.assertIsInstance(users_functions.user_mfa_totp_enable(self.UNITTEST_USER, False), dict)

    # test errors
    def test_users_user_mfa_totp_enable_error_input_null_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_mfa_totp_enable(None)

    def test_users_user_mfa_totp_enable_error_input_invalid_type_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_mfa_totp_enable(1)

    def test_users_user_mfa_totp_enable_error_input_invalid_format_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_mfa_totp_enable('not a UUID')

    def test_users_user_mfa_totp_enable_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.user_mfa_totp_enable(self.username, False)


@arcimoto.runtime.handler
def test_users_user_mfa_totp_enable():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UsersUserMfaTotpEnableTestCase)
    ))


lambda_handler = test_users_user_mfa_totp_enable
