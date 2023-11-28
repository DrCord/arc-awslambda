import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GetVehicleShadowTestCase(unittest.TestCase):

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        # this only works with a real style VIN for some reason
        # arcimoto.tests.uuid_vin_get() won't work with iot for some reason
        cls.vin = 'DEV-7F7ATR312KER99999'
        arcimoto.tests.vehicle_create(cls.vin)
        vehicles_functions.provision_iot(cls.vin)
        vehicles_functions.provision_iot_certificate(cls.vin)
        vehicles_functions.update_shadow_document(cls.vin)

    @classmethod
    def tearDownClass(cls):
        vehicles_functions.unprovision_iot_certificate(cls.vin)
        vehicles_functions.unprovision_iot(cls.vin)
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_get_vehicle_shadow_success(self):
        self.assertIsInstance(vehicles_functions.get_vehicle_shadow(self.vin), dict)

    # test errors
    def test_get_vehicle_shadow_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.get_vehicle_shadow(None)

    def test_get_vehicle_shadow_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.get_vehicle_shadow(1)

    def test_get_vehicle_shadow_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            vehicles_functions.get_vehicle_shadow(self.vin_invalid)


@arcimoto.runtime.handler
def test_get_vehicle_shadow():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(GetVehicleShadowTestCase)
    ))


lambda_handler = test_get_vehicle_shadow
