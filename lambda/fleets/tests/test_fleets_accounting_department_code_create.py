
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions


class FleetsAccountingDepartmentCodeCreateTestCase(unittest.TestCase):

    def test_fleets_accounting_department_code_create_success(self):
        adc_id = fleets_functions.accounting_department_code_create({'code': 'test_2', 'description': 'test desc'})
        self.assertTrue(adc_id is not None)
        fleets_functions.accounting_department_code_delete({'id': adc_id.get('id', None)})

    # test errors
    def test_fleets_accounting_department_code_create_error_input_null(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.accounting_department_code_create({})

    def test_vehicle_group_create_error_input_invalid_type(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.accounting_department_code_create({'code': 1})

    def test_vehicle_group_create_user_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            fleets_functions.accounting_department_code_create({'code': 'test_3', 'description': 'test desc'}, False)


@arcimoto.runtime.handler
def test_fleets_accounting_department_code_create():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(FleetsAccountingDepartmentCodeCreateTestCase)
    ))


lambda_handler = test_fleets_accounting_department_code_create
