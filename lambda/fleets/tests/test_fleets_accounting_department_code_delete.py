import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions


class FleetsAccountingDepartmentCodeDeleteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.accounting_department_code_id = fleets_functions.accounting_department_code_create({'code': 'test_1', 'description': 'test desc'})

    def test_fleets_accounting_department_code_delete_success(self):
        self.assertIsInstance(fleets_functions.accounting_department_code_delete(self.accounting_department_code_id), dict)

    # test errors
    def test_fleets_accounting_department_code_delete_error_input_no_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.accounting_department_code_delete({})

    def test_fleets_accounting_department_code_delete_error_input_invalid_type_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.accounting_department_code_delete({'id': 'Not an Integer'})

    def test_fleets_accounting_department_code_delete_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            fleets_functions.accounting_department_code_delete({'id': 999}, False)


@arcimoto.runtime.handler
def test_fleets_accounting_department_code_delete():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(FleetsAccountingDepartmentCodeDeleteTestCase)
    ))


lambda_handler = test_fleets_accounting_department_code_delete
