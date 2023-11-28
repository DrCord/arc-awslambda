import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehiclesModelReleasePartsGetTestCase(unittest.TestCase):

    MODEL_RELEASE_ID = 1

    def test_vehicles_model_release_parts_get_success(self):
        self.assertIsInstance(vehicles_functions.parts_get(self.MODEL_RELEASE_ID), dict)

    # test errors
    def test_vehicles_model_release_parts_get_error_null_model_release_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.parts_get(None)

    def test_vehicles_model_release_parts_get_error_invalid_model_release_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.parts_get(0)

    def test_vehicles_model_release_parts_get_error_invalid_type_model_release_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.parts_get('not an integer')

    def test_vehicles_model_release_parts_get_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.parts_get(self.MODEL_RELEASE_ID, False)


@arcimoto.runtime.handler
def test_vehicles_model_release_parts_get():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehiclesModelReleasePartsGetTestCase)
    ))


lambda_handler = test_vehicles_model_release_parts_get
