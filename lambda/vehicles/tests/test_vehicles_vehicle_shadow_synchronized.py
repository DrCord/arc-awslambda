import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehiclesVehicleShadowSynchronizedTestCase(unittest.TestCase):

    MODEL_RELEASE_ID = 1
    vin = None

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin, cls.MODEL_RELEASE_ID)
        vehicles_functions.provision_iot(cls.vin)
        vehicles_functions.provision_iot_certificate(cls.vin)
        vehicles_functions.update_shadow_document(cls.vin)

    def test_vehicles_vehicle_shadow_synchronized_success(self):
        self.assertIsInstance(vehicles_functions.vehicle_shadow_synchronized(self.vin), dict)

    # test errors
    def test_vehicles_vehicle_shadow_synchronized_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.vehicle_shadow_synchronized(None)

    def test_vehicles_vehicle_shadow_synchronized_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            vehicles_functions.vehicle_shadow_synchronized(self.vin_invalid)

    def test_vehicles_vehicle_shadow_synchronized_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.vehicle_shadow_synchronized(1)

    def test_vehicles_vehicle_shadow_synchronized_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.vehicle_shadow_synchronized(self.vin, False)


@arcimoto.runtime.handler
def test_vehicles_vehicle_shadow_synchronized():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehiclesVehicleShadowSynchronizedTestCase)
    ))


lambda_handler = test_vehicles_vehicle_shadow_synchronized
