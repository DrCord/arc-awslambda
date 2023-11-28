import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import authorities_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SignVehicleTokenTestCase(unittest.TestCase):

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @property
    def authority_id_invalid(self):
        return authorities_functions.authorities_highest_id() + 1

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        cls.vin2 = arcimoto.tests.uuid_vin_get()
        cls.authority_id = authorities_functions.create_authority().get('id', None)
        cls.authority_id2 = authorities_functions.create_authority().get('id', None)
        # this cannot be cleaned up, the arcimoto authority cannot be removed from a vehicle
        authorities_functions.provision_vehicle_authority(authorities_functions.ARCIMOTO_AUTHORITY_ID, cls.vin)
        authorities_functions.provision_vehicle_authority(authorities_functions.ARCIMOTO_AUTHORITY_ID, cls.vin2)
        authorities_functions.provision_vehicle_authority(cls.authority_id, cls.vin)
        authorities_functions.provision_vehicle_authority(cls.authority_id2, cls.vin2)

    @classmethod
    def tearDownClass(cls):
        if cls.authority_id is not None:
            authorities_functions.unprovision_vehicle_authority(cls.authority_id, cls.vin)
            authorities_functions.unprovision_vehicle_authority(cls.authority_id2, cls.vin2)
            authorities_functions.delete_authority(cls.authority_id)
            authorities_functions.delete_authority(cls.authority_id2)

    def test_sign_vehicle_token_success(self):
        self.assertIsInstance(authorities_functions.sign_vehicle_token(self.authority_id, {'vin': self.vin}), dict)

    # test errors
    def test_sign_vehicle_token_error_no_authority_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.sign_vehicle_token(None, {'vin': self.vin})

    def test_sign_vehicle_token_error_no_token(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.sign_vehicle_token(self.authority_id, None)

    def test_sign_vehicle_token_error_vin_not_present_in_token(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.sign_vehicle_token(self.authority_id, {})

    def test_sign_vehicle_token_error_no_matching_authority_found(self):
        with self.assertRaises(ArcimotoNotFoundError):
            authorities_functions.sign_vehicle_token(self.authority_id_invalid, {'vin': self.vin})

    def test_sign_vehicle_token_error_vin_does_not_exist(self):
        with self.assertRaises(ArcimotoNotFoundError):
            authorities_functions.sign_vehicle_token(self.authority_id, {'vin': self.vin_invalid})

    def test_sign_vehicle_token_error_authority_does_not_control_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.sign_vehicle_token(self.authority_id, {'vin': self.vin2})

    def test_sign_vehicle_token_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            authorities_functions.sign_vehicle_token(self.authority_id, {'vin': self.vin}, False)


@arcimoto.runtime.handler
def test_sign_vehicle_token():
    return arcimoto.tests.handle_test_result(
        unittest.TextTestRunner().run(
            unittest.TestLoader().loadTestsFromTestCase(SignVehicleTokenTestCase)
        ))


lambda_handler = test_sign_vehicle_token
