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


class UsersUserMfaTotpAssociateTokenTestCase(unittest.TestCase):

    # this would need to be a real token for the success tests
    access_token = 'test123'

    # disabled to potentially enable later, but cannot pass as needs a logged in user access token
    # def test_users_user_mfa_totp_associate_token_success(self):
    #     self.assertIsInstance(users_functions.user_mfa_totp_associate_token(self.access_token), dict)

    # test errors
    def test_users_user_mfa_totp_associate_token_error_input_null_access_token(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_mfa_totp_associate_token(None)

    def test_users_user_mfa_totp_associate_token_error_input_invalid_type_access_token(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_mfa_totp_associate_token(1)

    def test_users_user_mfa_totp_associate_token_error_input_empty_access_token(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_mfa_totp_associate_token('')


@arcimoto.runtime.handler
def test_users_user_mfa_totp_associate_token():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UsersUserMfaTotpAssociateTokenTestCase)
    ))


lambda_handler = test_users_user_mfa_totp_associate_token
