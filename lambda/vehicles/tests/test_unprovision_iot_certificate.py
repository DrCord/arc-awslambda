import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UnprovisionIoTCertificateTestCase(unittest.TestCase):

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)
        vehicles_functions.provision_iot(cls.vin)
        vehicles_functions.provision_iot_certificate(cls.vin)

    @classmethod
    def tearDownClass(cls):
        vehicles_functions.unprovision_iot(cls.vin)
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_unprovision_iot_certificate_success(self):
        self.assertIsInstance(vehicles_functions.unprovision_iot_certificate(self.vin), dict)

    # test errors
    def test_unprovision_iot_certificate_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.unprovision_iot_certificate(None)

    def test_unprovision_iot_certificate_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            vehicles_functions.unprovision_iot_certificate(self.vin_invalid)

    def test_unprovision_iot_certificate_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.unprovision_iot_certificate(1)

    def test_unprovision_iot_certificate_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.unprovision_iot_certificate(self.vin, False)


@arcimoto.runtime.handler
def test_unprovision_iot_certificate():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UnprovisionIoTCertificateTestCase)
    ))


lambda_handler = test_unprovision_iot_certificate
