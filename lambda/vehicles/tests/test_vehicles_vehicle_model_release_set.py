import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehiclesVehicleModelReleaseSetTestCase(unittest.TestCase):

    MODEL_RELEASE_ID = 1

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin, cls.MODEL_RELEASE_ID)

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_vehicles_vehicle_model_release_set_success(self):
        self.assertIsInstance(vehicles_functions.vehicle_model_release_set(self.vin, self.MODEL_RELEASE_ID), dict)

    # test errors
    def test_vehicles_vehicle_model_release_set_error_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.vehicle_model_release_set(None, self.MODEL_RELEASE_ID)

    def test_vehicles_vehicle_model_release_set_error_null_model_release_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.vehicle_model_release_set(self.vin, None)

    def test_vehicles_vehicle_model_release_set_error_invalid_model_release_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.vehicle_model_release_set(self.vin, 0)

    def test_vehicles_vehicle_model_release_set_error_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            vehicles_functions.vehicle_model_release_set(self.vin_invalid, self.MODEL_RELEASE_ID)

    def test_vehicles_vehicle_model_release_set_error_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.vehicle_model_release_set(0, self.MODEL_RELEASE_ID)

    def test_vehicles_vehicle_model_release_set_error_invalid_type_model_release_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.vehicle_model_release_set(self.vin, 'not an integer')

    def test_vehicles_vehicle_model_release_set_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.vehicle_model_release_set(self.vin, self.MODEL_RELEASE_ID, False)


@arcimoto.runtime.handler
def test_vehicles_vehicle_model_release_set():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehiclesVehicleModelReleaseSetTestCase)
    ))


lambda_handler = test_vehicles_vehicle_model_release_set
