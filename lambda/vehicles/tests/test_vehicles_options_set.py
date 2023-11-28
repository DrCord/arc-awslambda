import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehiclesOptionsSetTestCase(unittest.TestCase):

    options = {
        'heated_seats': 'true',
        'heated_grips': 'true',
        'stereo_enabled': 'true'
    }

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_vehicles_options_set_success(self):
        self.assertIsInstance(vehicles_functions.vehicles_options_set(self.vin, self.options), dict)

    # test errors
    def test_vehicles_options_set_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.vehicles_options_set(None, self.options)

    def test_vehicles_options_set_error_input_null_options(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.vehicles_options_set(self.vin, None)

    def test_vehicles_options_set_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            vehicles_functions.vehicles_options_set(self.vin_invalid, self.options)

    def test_vehicles_options_set_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.vehicles_options_set(1, self.options)

    def test_vehicles_options_set_error_input_invalid_type_options(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.vehicles_options_set(self.vin, 'not a dictionary')

    def test_vehicles_options_set_error_input_empty_options(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.vehicles_options_set(self.vin, {})

    def test_vehicles_options_set_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.vehicles_options_set(self.vin, self.options, False)


@arcimoto.runtime.handler
def test_vehicles_options_set():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehiclesOptionsSetTestCase)
    ))


lambda_handler = test_vehicles_options_set
