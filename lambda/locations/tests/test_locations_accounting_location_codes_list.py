import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import locations_functions


class LocationsAccountingLocationCodesListTestCase(unittest.TestCase):

    def test_accounting_locations_list_success(self):
        self.assertIsInstance(locations_functions.accounting_location_codes_list(), dict)


@arcimoto.runtime.handler
def test_locations_accounting_location_codes_list():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(LocationsAccountingLocationCodesListTestCase)
    ))


lambda_handler = test_locations_accounting_location_codes_list
