import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import authorities_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AuthkeyVehicleGetTestCase(unittest.TestCase):

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        authorities_functions.provision_vehicle_authority(authorities_functions.ARCIMOTO_AUTHORITY_ID, cls.vin)
        authorities_functions.factory_pin_generate(cls.vin)

    @classmethod
    def tearDownClass(cls):
        authorities_functions.unprovision_vehicle_arcimoto_authority(cls.vin)

    def test_authkey_vehicle_get_success(self):
        self.assertIsInstance(authorities_functions.authkey_vehicle_get(self.vin), dict)

    # test errors
    def test_authkey_vehicle_get_error_no_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.authkey_vehicle_get(None)

    def test_authkey_vehicle_get_error_vin_does_not_exist(self):
        with self.assertRaises(ArcimotoNotFoundError):
            authorities_functions.authkey_vehicle_get(self.vin_invalid)

    def test_authkey_vehicle_get_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            authorities_functions.authkey_vehicle_get(self.vin, False)


@arcimoto.runtime.handler
def test_authkey_vehicle_get():
    return arcimoto.tests.handle_test_result(
        unittest.TextTestRunner().run(
            unittest.TestLoader().loadTestsFromTestCase(AuthkeyVehicleGetTestCase)
        ))


lambda_handler = test_authkey_vehicle_get
