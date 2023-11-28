import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import locations_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LocationsCountriesListTestCase(unittest.TestCase):

    def test_locations_countries_list_success(self):
        self.assertIsInstance(locations_functions.countries_list(), dict)


@arcimoto.runtime.handler
def test_locations_countries_list():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(LocationsCountriesListTestCase)
    ))


lambda_handler = test_locations_countries_list
