import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import authorities_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UnprovisionVehicleArcimotoAuthorityTestCase(unittest.TestCase):

    vin = None

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        authorities_functions.provision_vehicle_authority(authorities_functions.ARCIMOTO_AUTHORITY_ID, cls.vin)

    def test_unprovision_vehicle_arcimoto_authority_success(self):
        self.assertIsInstance(authorities_functions.unprovision_vehicle_arcimoto_authority(self.vin), dict)

    # test errors
    def test_unprovision_vehicle_arcimoto_authority_error_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.unprovision_vehicle_arcimoto_authority(None)

    def test_create_authority_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            authorities_functions.unprovision_vehicle_arcimoto_authority(self.vin, False)


@arcimoto.runtime.handler
def test_unprovision_vehicle_arcimoto_authority():

    return arcimoto.tests.handle_test_result(
        unittest.TextTestRunner().run(
            unittest.TestLoader().loadTestsFromTestCase(UnprovisionVehicleArcimotoAuthorityTestCase)
        ))


lambda_handler = test_unprovision_vehicle_arcimoto_authority
