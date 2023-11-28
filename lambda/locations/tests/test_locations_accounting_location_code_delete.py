import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import locations_functions


class LocationsAccountingLocationCodeDeleteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.accounting_location_code_id = locations_functions.accounting_location_code_create({'code': 'test_1'})

    def test_locations_accounting_location_code_delete_success(self):
        self.assertIsInstance(locations_functions.accounting_location_code_delete(self.accounting_location_code_id), dict)

    # test errors
    def test_locations_accounting_location_code_delete_error_input_no_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.accounting_location_code_delete({})

    def test_locations_accounting_location_code_delete_error_input_invalid_type_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.accounting_location_code_delete({'id': 'Not an Integer'})

    def test_locations_accounting_location_code_delete_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            locations_functions.accounting_location_code_delete(self.accounting_location_code_id, False)


@arcimoto.runtime.handler
def test_locations_accounting_location_code_delete():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(LocationsAccountingLocationCodeDeleteTestCase)
    ))


lambda_handler = test_locations_accounting_location_code_delete
