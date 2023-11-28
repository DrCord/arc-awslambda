import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions
import reef_functions
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ReefVehicleShadowSynchronizedTestCase(unittest.TestCase):

    MODEL_RELEASE_ID = 1
    REEF_VEHICLE_GROUP_ID = reef_functions.REEF_VEHICLE_GROUP_ID
    vin = None

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin, cls.MODEL_RELEASE_ID)
        fleets_functions.vehicle_group_add_vehicle(cls.REEF_VEHICLE_GROUP_ID, cls.vin)
        vehicles_functions.provision_iot(cls.vin)
        vehicles_functions.provision_iot_certificate(cls.vin)
        vehicles_functions.update_shadow_document(cls.vin)

    @classmethod
    def tearDownClass(cls):
        fleets_functions.vehicle_group_remove_vehicle(cls.REEF_VEHICLE_GROUP_ID, cls.vin)
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_reef_vehicle_shadow_synchronized_success(self):
        self.assertIsInstance(reef_functions.vehicle_shadow_synchronized(self.vin), dict)

    # test errors
    def test_reef_vehicle_shadow_synchronized_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.vehicle_shadow_synchronized(None)

    def test_reef_vehicle_shadow_synchronized_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.vehicle_shadow_synchronized(1)

    # unauthorized check comes before vin validity check, so invalid VINs are unauthorized
    def test_reef_vehicle_shadow_synchronized_error_unauthorized_for_vin(self):
        with self.assertRaises(ArcimotoPermissionError):
            reef_functions.vehicle_shadow_synchronized(self.vin_invalid)

    # to test an invalid vin it must be allowed by the REEF vehicle group
    def test_reef_vehicle_shadow_synchronized_error_input_invalid_vin(self):
        invalid_allowed_vin = self.vin_invalid
        reef_functions.add_invalid_vin_directly_to_vehicle_group(invalid_allowed_vin)
        with self.assertRaises(ArcimotoNotFoundError):
            reef_functions.vehicle_shadow_synchronized(invalid_allowed_vin)
        reef_functions.remove_invalid_vin_directly_from_vehicle_group(invalid_allowed_vin)


@arcimoto.runtime.handler
def test_reef_vehicle_shadow_synchronized():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ReefVehicleShadowSynchronizedTestCase)
    ))


lambda_handler = test_reef_vehicle_shadow_synchronized
