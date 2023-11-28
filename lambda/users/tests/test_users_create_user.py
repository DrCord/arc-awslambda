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


class UsersCreateUserTestCase(unittest.TestCase):

    args = {
        'email': 'unittest' + uuid.uuid4().hex + '@arcimoto.com',
        'phone': '+15415551212',
        'display_name': 'Unit Test User'
    }

    def test_users_create_user_success(self):
        username = users_functions.user_create(self.args).get('username', None)
        self.assertIsNotNone(username)
        users_functions.user_delete(username)

    # test errors
    def test_users_create_user_error_input_null_email(self):
        args = copy.deepcopy(self.args)
        args['email'] = None
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_create(args)

    def test_users_create_user_error_input_null_phone(self):
        args = copy.deepcopy(self.args)
        args['phone'] = None
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_create(args)

    def test_users_create_user_error_input_null_display_name(self):
        args = copy.deepcopy(self.args)
        args['display_name'] = None
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_create(args)

    def test_users_create_user_error_input_invalid_type_email(self):
        args = copy.deepcopy(self.args)
        args['email'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_create(args)

    def test_users_create_user_error_input_invalid_type_phone(self):
        args = copy.deepcopy(self.args)
        args['phone'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_create(args)

    def test_users_create_user_error_input_invalid_type_display_name(self):
        args = copy.deepcopy(self.args)
        args['display_name'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_create(args)

    def test_users_create_user_error_input_invalid_format_email(self):
        args = copy.deepcopy(self.args)
        args['email'] = 'unittest.com'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_create(args)
        args['email'] = 'unittest@com.'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_create(args)
        args['email'] = '@unit@test.com'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_create(args)
        args['email'] = 'unit@test.com/'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_create(args)
        args['email'] = 'unittestcom'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_create(args)
        args['email'] = 'unit@test..com'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_create(args)

    def test_users_create_user_error_input_invalid_format_phone(self):
        args = copy.deepcopy(self.args)
        args['phone'] = '(541) 555-1212'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_create(args)
        args['phone'] = '1(541) 555-1212'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_create(args)
        args['phone'] = '5415551212'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_create(args)
        args['phone'] = '15415551212'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_create(args)
        args['phone'] = '(541)555-1212'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.user_create(args)

    def test_users_create_user_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.user_create(self.args, False)


@arcimoto.runtime.handler
def test_users_create_user():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UsersCreateUserTestCase)
    ))


lambda_handler = test_users_create_user
