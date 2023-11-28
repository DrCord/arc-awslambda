import logging
import unittest
import uuid
import copy
import base64

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import users_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UsersProfileUpdateTestCase(unittest.TestCase):

    args = {
        'username': None,
        'email': 'unittest' + uuid.uuid4().hex + '@arcimoto.com',
        'phone': '+19876543210',
        'display_name': 'Unit Tester Edited',
        'avatar': f'data:image/jpeg;base64,{str(base64.b64encode(uuid.uuid4().bytes))}'
    }

    @property
    def test_email(self):
        return 'unittest' + uuid.uuid4().hex + '@arcimoto.com'

    @classmethod
    def setUpClass(cls):
        args = {
            'email': 'unittest' + uuid.uuid4().hex + '@arcimoto.com',
            'phone': '+15415551212',
            'display_name': 'Unit Test User'
        }
        cls.UNITTEST_USER = arcimoto.tests.unit_test_user_get_username()
        cls.username = users_functions.user_create(args).get('username', None)
        cls.args['username'] = cls.username

    @classmethod
    def tearDownClass(cls):
        users_functions.user_delete(cls.username)

    def test_users_profile_update_success(self):
        args = copy.deepcopy(self.args)
        self.assertIsInstance(users_functions.profile_update(args), dict)

    def test_users_profile_update_success_edit_own_user(self):
        args = copy.deepcopy(self.args)
        args['username'] = self.UNITTEST_USER
        args['email'] = self.test_email
        self.assertIsInstance(users_functions.profile_update(args, False), dict)
        # restore data after edit
        args['display_name'] = 'Unit Tester'
        args['email'] = 'unittest@arcimoto.com'
        users_functions.profile_update(args, False)

    # test errors
    def test_users_profile_update_error_input_null_username(self):
        args = copy.deepcopy(self.args)
        args['username'] = None
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_update(args)

    def test_users_profile_update_error_input_invalid_type_username(self):
        args = copy.deepcopy(self.args)
        args['username'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_update(args)

    def test_users_profile_update_error_input_invalid_type_email(self):
        args = copy.deepcopy(self.args)
        args['email'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_update(args)

    def test_users_profile_update_error_input_invalid_type_phone(self):
        args = copy.deepcopy(self.args)
        args['phone'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_update(args)

    def test_users_profile_update_error_input_invalid_type_display_name(self):
        args = copy.deepcopy(self.args)
        args['display_name'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_update(args)

    def test_users_profile_update_error_input_invalid_type_avatar(self):
        args = copy.deepcopy(self.args)
        args['avatar'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_update(args)

    def test_users_profile_update_error_input_invalid_format_username(self):
        args = copy.deepcopy(self.args)
        args['username'] = 'not a UUID'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_update(args)

    def test_users_profile_update_error_input_invalid_format_email(self):
        args = copy.deepcopy(self.args)
        args['email'] = 'unittest.com'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_update(args)
        args['email'] = 'unittest@com.'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_update(args)
        args['email'] = '@unit@test.com'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_update(args)
        args['email'] = 'unit@test.com/'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_update(args)
        args['email'] = 'unittestcom'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_update(args)
        args['email'] = 'unit@test..com'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_update(args)

    def test_users_profile_update_error_input_invalid_format_phone(self):
        args = copy.deepcopy(self.args)
        args['phone'] = '(541) 555-1212'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_update(args)
        args['phone'] = '1(541) 555-1212'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_update(args)
        args['phone'] = '5415551212'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_update(args)
        args['phone'] = '15415551212'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_update(args)
        args['phone'] = '(541)555-1212'
        with self.assertRaises(ArcimotoArgumentError):
            users_functions.profile_update(args)

    def test_users_profile_update_error_user_unauthorized(self):
        args = copy.deepcopy(self.args)
        with self.assertRaises(ArcimotoPermissionError):
            users_functions.profile_update(args, False)


@arcimoto.runtime.handler
def test_users_profile_update():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UsersProfileUpdateTestCase)
    ))


lambda_handler = test_users_profile_update
