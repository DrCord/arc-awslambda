import logging
import unittest
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import arcimoto.db
import reef_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ReefSheerIdVerifyDLTestCase(unittest.TestCase):

    args = {
        'first_name': 'Unit',
        'last_name': 'McTester',
        'email': 'test@arcimoto.com',
        'drivers_license_number': '1234567',
        'state': 'OR'
    }

    def test_reef_sheer_id_verify_dl_success(self):
        self.assertIsInstance(reef_functions.verify_dl(self.args), dict)

    # test errors
    def test_reef_sheer_id_verify_dl_error_null_first_name(self):
        args = copy.deepcopy(self.args)
        args['first_name'] = None
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.verify_dl(args)

    def test_reef_sheer_id_verify_dl_error_null_last_name(self):
        args = copy.deepcopy(self.args)
        args['last_name'] = None
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.verify_dl(args)

    def test_reef_sheer_id_verify_dl_error_null_email(self):
        args = copy.deepcopy(self.args)
        args['email'] = None
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.verify_dl(args)

    def test_reef_sheer_id_verify_dl_error_null_drivers_license_number(self):
        args = copy.deepcopy(self.args)
        args['drivers_license_number'] = None
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.verify_dl(args)

    def test_reef_sheer_id_verify_dl_error_null_state(self):
        args = copy.deepcopy(self.args)
        args['state'] = None
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.verify_dl(args)

    def test_reef_sheer_id_verify_dl_error_invalid_type_first_name(self):
        args = copy.deepcopy(self.args)
        args['first_name'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.verify_dl(args)

    def test_reef_sheer_id_verify_dl_error_invalid_type_last_name(self):
        args = copy.deepcopy(self.args)
        args['last_name'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.verify_dl(args)

    def test_reef_sheer_id_verify_dl_error_invalid_type_email(self):
        args = copy.deepcopy(self.args)
        args['email'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.verify_dl(args)

    def test_reef_sheer_id_verify_dl_error_invalid_type_drivers_license_number(self):
        args = copy.deepcopy(self.args)
        args['drivers_license_number'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.verify_dl(args)

    def test_reef_sheer_id_verify_dl_error_invalid_type_state(self):
        args = copy.deepcopy(self.args)
        args['state'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.verify_dl(args)

    def test_reef_sheer_id_verify_dl_error_empty_first_name(self):
        args = copy.deepcopy(self.args)
        args['first_name'] = ''
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.verify_dl(args)

    def test_reef_sheer_id_verify_dl_error_empty_last_name(self):
        args = copy.deepcopy(self.args)
        args['last_name'] = ''
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.verify_dl(args)

    def test_reef_sheer_id_verify_dl_error_empty_email(self):
        args = copy.deepcopy(self.args)
        args['email'] = ''
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.verify_dl(args)

    def test_reef_sheer_id_verify_dl_error_empty_drivers_license_number(self):
        args = copy.deepcopy(self.args)
        args['drivers_license_number'] = ''
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.verify_dl(args)

    def test_reef_sheer_id_verify_dl_error_empty_state(self):
        args = copy.deepcopy(self.args)
        args['state'] = ''
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.verify_dl(args)


@arcimoto.runtime.handler
def test_reef_sheer_id_verify_dl():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(
            ReefSheerIdVerifyDLTestCase)))


lambda_handler = test_reef_sheer_id_verify_dl
