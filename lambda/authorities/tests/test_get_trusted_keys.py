import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import authorities_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GetTrustedKeysTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        # this cannot be cleaned up, the arcimoto authority cannot be removed from a vehicle
        authorities_functions.provision_vehicle_authority(authorities_functions.ARCIMOTO_AUTHORITY_ID, cls.vin)

    def test_get_trusted_keys_success(self):
        self.assertTrue(len(authorities_functions.get_trusted_keys(self.vin)) > 0)

    # test errors
    def test_get_trusted_keys_error_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.get_trusted_keys(None)


@arcimoto.runtime.handler
def test_get_trusted_keys():
    return arcimoto.tests.handle_test_result(
        unittest.TextTestRunner().run(
            unittest.TestLoader().loadTestsFromTestCase(GetTrustedKeysTestCase)
        ))


lambda_handler = test_get_trusted_keys
