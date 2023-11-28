import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import locations_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LocationsAddressTypesListTestCase(unittest.TestCase):

    def test_locations_address_types_list_success(self):
        self.assertIsInstance(locations_functions.address_types_list(), dict)


@arcimoto.runtime.handler
def test_locations_address_types_list():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(LocationsAddressTypesListTestCase)
    ))


lambda_handler = test_locations_address_types_list
