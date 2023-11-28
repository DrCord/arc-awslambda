import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehiclesModelReleasesListTestCase(unittest.TestCase):

    def test_vehicles_model_releases_list_success_model_id_null(self):
        self.assertIsInstance(vehicles_functions.model_releases_list(), dict)

    def test_vehicles_model_releases_list_success_input_model_id(self):
        self.assertIsInstance(vehicles_functions.model_releases_list(1), dict)

    # test errors
    def test_vehicles_model_releases_list_error_input_invalid_model_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.model_releases_list(-1)

    def test_vehicles_model_releases_list_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.model_releases_list(1, False)


@arcimoto.runtime.handler
def test_vehicles_model_releases_list():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehiclesModelReleasesListTestCase)
    ))


lambda_handler = test_vehicles_model_releases_list
