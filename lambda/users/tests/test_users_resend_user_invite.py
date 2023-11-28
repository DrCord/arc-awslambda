import logging
import unittest
import copy
import uuid
import boto3

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import users_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UsersResendUserInviteTestCase(unittest.TestCase):

    args = {
        'email': 'unittest+' + uuid.uuid4().hex + '@arcimoto.com',
        'phone': '+15415551212',
        'display_name': 'Unit Test User'
    }
    username = None

    @classmethod
    def setUpClass(cls):
        cls.username = users_functions.user_create(cls.args).get('username', None)

    @classmethod
    def tearDownClass(cls):
        users_functions.user_delete(cls.username)

    def test_users_resend_user_invite_success(self):
        self.assertIsInstance(users_functions.user_resend_invite(self.username), dict)

    # test errors
    def test_users_resend_user_invite_error_input_null_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_resend_invite(None)

    def test_users_resend_user_invite_error_input_invalid_type_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_resend_invite(1)

    def test_users_resend_user_invite_error_input_invalid_format_username(self):
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_resend_invite('not a username UUID')

    def test_users_resend_user_invite_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.user_resend_invite(self.username, False)


@arcimoto.runtime.handler
def test_users_resend_user_invite():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UsersResendUserInviteTestCase)
    ))


lambda_handler = test_users_resend_user_invite
