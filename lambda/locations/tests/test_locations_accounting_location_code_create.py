
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import locations_functions


class LocationsAccountingLocationCodeCreateTestCase(unittest.TestCase):

    def test_locations_accounting_location_code_create_success(self):
        al_id = locations_functions.accounting_location_code_create({'code': 'test1'})
        self.assertTrue(al_id is not None)
        locations_functions.accounting_location_code_delete({'id': al_id.get('id', None)})

    # test errors
    def test_locations_accounting_location_code_create_error_input_null(self):
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.accounting_location_code_create({})

    def test_locations_accounting_location_create_error_input_invalid_type(self):
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.accounting_location_code_create({'code': 1})

    def test_locations_accounting_location_code_create_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            locations_functions.accounting_location_code_create({'code': 'UNAUTH'}, False)


@arcimoto.runtime.handler
def test_locations_accounting_location_code_create():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(LocationsAccountingLocationCodeCreateTestCase)
    ))


lambda_handler = test_locations_accounting_location_code_create
