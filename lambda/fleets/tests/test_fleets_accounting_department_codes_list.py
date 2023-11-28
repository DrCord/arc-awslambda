import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions


class FleetsAccountingDepartmentCodesListTestCase(unittest.TestCase):

    def test_vehicle_group_types_list_success(self):
        self.assertIsInstance(fleets_functions.accounting_department_codes_list(), dict)

    def test_vehicle_group_types_list_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            fleets_functions.accounting_department_codes_list(False)


@arcimoto.runtime.handler
def test_fleets_accounting_department_codes_list():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(FleetsAccountingDepartmentCodesListTestCase)
    ))


lambda_handler = test_fleets_accounting_department_codes_list
