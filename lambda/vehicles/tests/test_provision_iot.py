import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ProvisionIoTTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)

    @classmethod
    def tearDownClass(cls):
        vehicles_functions.unprovision_iot(cls.vin)
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_provision_iot_success(self):
        self.assertIsInstance(vehicles_functions.provision_iot(self.vin), dict)

    # test errors
    def test_provision_iot_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.provision_iot(None)

    def test_provision_iot_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.provision_iot(1)

    def test_provision_iot_error_input_vin_not_prefixed_correctly_for_dev_env(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.provision_iot('TEST-VIN')

    def test_provision_iot_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.provision_iot(self.vin, False)


@arcimoto.runtime.handler
def test_provision_iot():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ProvisionIoTTestCase)
    ))


lambda_handler = test_provision_iot
