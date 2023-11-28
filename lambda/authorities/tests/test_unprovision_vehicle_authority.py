import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import authorities_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UnprovisionVehicleAuthorityTestCase(unittest.TestCase):

    @property
    def authority_id_invalid(self):
        return authorities_functions.authorities_highest_id() + 1

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        cls.authority_id = authorities_functions.create_authority().get('id', None)
        cls.authority_id2 = authorities_functions.create_authority('Unit Tester 2', cls.authority_id).get('id', None)
        # this cannot be cleaned up, the arcimoto authority cannot be removed from a vehicle
        authorities_functions.provision_vehicle_authority(authorities_functions.ARCIMOTO_AUTHORITY_ID, cls.vin)
        authorities_functions.provision_vehicle_authority(cls.authority_id, cls.vin)

    @classmethod
    def tearDownClass(cls):
        if cls.authority_id2 is not None:
            authorities_functions.delete_authority(cls.authority_id2)
        if cls.authority_id is not None:
            authorities_functions.delete_authority(cls.authority_id)

    def test_unprovision_vehicle_authority_success(self):
        self.assertIsInstance(authorities_functions.unprovision_vehicle_authority(self.authority_id, self.vin), dict)

    # test errors
    def test_unprovision_vehicle_authority_error_null_authority_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.unprovision_vehicle_authority(None, self.vin)

    def test_unprovision_vehicle_authority_error_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.unprovision_vehicle_authority(self.authority_id, None)

    def test_unprovision_vehicle_authority_error_invalid_authority_id_must_be_positive_integer(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.unprovision_vehicle_authority(-1, self.vin)

    def test_unprovision_vehicle_authority_error_invalid_authority_id_arcimoto(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.unprovision_vehicle_authority(authorities_functions.ARCIMOTO_AUTHORITY_ID, self.vin)

    def test_unprovision_vehicle_authority_error_authority_does_not_exist(self):
        with self.assertRaises(ArcimotoNotFoundError):
            authorities_functions.unprovision_vehicle_authority(self.authority_id_invalid, self.vin)

    def test_create_authority_error_authority_does_not_control_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.unprovision_vehicle_authority(self.authority_id2, self.vin)

    def test_create_authority_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            authorities_functions.unprovision_vehicle_authority(self.authority_id, self.vin, False)

    # not testable
    # Unprovision input parameters didn't match single database authority record
    # this would demonstrate a problem with the db records and is not readily testable in our setup


@arcimoto.runtime.handler
def test_unprovision_vehicle_authority():

    return arcimoto.tests.handle_test_result(
        unittest.TextTestRunner().run(
            unittest.TestLoader().loadTestsFromTestCase(UnprovisionVehicleAuthorityTestCase)
        ))


lambda_handler = test_unprovision_vehicle_authority
