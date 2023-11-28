import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehiclesModelsListTestCase(unittest.TestCase):

    def test_vehicles_models_list_success_platform_id_null(self):
        self.assertIsInstance(vehicles_functions.models_list(), dict)

    def test_vehicles_models_list_success_input_platform_id(self):
        self.assertIsInstance(vehicles_functions.models_list(1), dict)

    # test errors
    def test_vehicles_models_list_error_input_invalid_platform_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.models_list(-1)


@arcimoto.runtime.handler
def test_vehicles_models_list():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehiclesModelsListTestCase)
    ))


lambda_handler = test_vehicles_models_list
