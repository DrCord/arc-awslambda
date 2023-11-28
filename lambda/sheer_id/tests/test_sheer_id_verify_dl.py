import logging
import unittest
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import arcimoto.db
import sheer_id_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SheerIdVerifyDLTestCase(unittest.TestCase):

    args = {
        'first_name': 'Person',
        'last_name': 'McArcimoto',
        'email': 'test@arcimoto.com',
        'drivers_license_number': '1234567',
        'state': 'OR'
    }

    def test_sheer_id_verify_dl_success(self):
        self.assertIsInstance(sheer_id_functions.verify_dl(self.args), dict)

    # test errors
    def test_sheer_id_verify_dl_error_null_first_name(self):
        args = copy.deepcopy(self.args)
        args['first_name'] = None
        with self.assertRaises(ArcimotoArgumentError):
            sheer_id_functions.verify_dl(args)

    def test_sheer_id_verify_dl_error_null_last_name(self):
        args = copy.deepcopy(self.args)
        args['last_name'] = None
        with self.assertRaises(ArcimotoArgumentError):
            sheer_id_functions.verify_dl(args)

    def test_sheer_id_verify_dl_error_null_email(self):
        args = copy.deepcopy(self.args)
        args['email'] = None
        with self.assertRaises(ArcimotoArgumentError):
            sheer_id_functions.verify_dl(args)

    def test_sheer_id_verify_dl_error_null_drivers_license_number(self):
        args = copy.deepcopy(self.args)
        args['drivers_license_number'] = None
        with self.assertRaises(ArcimotoArgumentError):
            sheer_id_functions.verify_dl(args)

    def test_sheer_id_verify_dl_error_null_state(self):
        args = copy.deepcopy(self.args)
        args['state'] = None
        with self.assertRaises(ArcimotoArgumentError):
            sheer_id_functions.verify_dl(args)

    def test_sheer_id_verify_dl_error_invalid_type_first_name(self):
        args = copy.deepcopy(self.args)
        args['first_name'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            sheer_id_functions.verify_dl(args)

    def test_sheer_id_verify_dl_error_invalid_type_last_name(self):
        args = copy.deepcopy(self.args)
        args['last_name'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            sheer_id_functions.verify_dl(args)

    def test_sheer_id_verify_dl_error_invalid_type_email(self):
        args = copy.deepcopy(self.args)
        args['email'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            sheer_id_functions.verify_dl(args)

    def test_sheer_id_verify_dl_error_invalid_type_drivers_license_number(self):
        args = copy.deepcopy(self.args)
        args['drivers_license_number'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            sheer_id_functions.verify_dl(args)

    def test_sheer_id_verify_dl_error_invalid_type_state(self):
        args = copy.deepcopy(self.args)
        args['state'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            sheer_id_functions.verify_dl(args)

    def test_sheer_id_verify_dl_error_empty_first_name(self):
        args = copy.deepcopy(self.args)
        args['first_name'] = ''
        with self.assertRaises(ArcimotoArgumentError):
            sheer_id_functions.verify_dl(args)

    def test_sheer_id_verify_dl_error_empty_last_name(self):
        args = copy.deepcopy(self.args)
        args['last_name'] = ''
        with self.assertRaises(ArcimotoArgumentError):
            sheer_id_functions.verify_dl(args)

    def test_sheer_id_verify_dl_error_empty_email(self):
        args = copy.deepcopy(self.args)
        args['email'] = ''
        with self.assertRaises(ArcimotoArgumentError):
            sheer_id_functions.verify_dl(args)

    def test_sheer_id_verify_dl_error_empty_drivers_license_number(self):
        args = copy.deepcopy(self.args)
        args['drivers_license_number'] = ''
        with self.assertRaises(ArcimotoArgumentError):
            sheer_id_functions.verify_dl(args)

    def test_sheer_id_verify_dl_error_empty_state(self):
        args = copy.deepcopy(self.args)
        args['state'] = ''
        with self.assertRaises(ArcimotoArgumentError):
            sheer_id_functions.verify_dl(args)

    def test_sheer_id_verify_dl_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            sheer_id_functions.verify_dl(self.args, False)


@arcimoto.runtime.handler
def test_sheer_id_verify_dl():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(
            SheerIdVerifyDLTestCase)))


lambda_handler = test_sheer_id_verify_dl
