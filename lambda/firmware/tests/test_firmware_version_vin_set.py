import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import firmware_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class FirmwareVersionVinSetTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.test_vin)
        firmware_versions_release_data_response = firmware_functions.firmware_version_get_release_data('deployedfirmware')
        cls.updated_firmware = firmware_functions.firmware_version_set_release_data(firmware_versions_release_data_response)

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.test_vin)

    def test_firmware_version_vin_set_success(self):
        vin_firmware_versions = firmware_functions.firmware_version_vin_set({'vin': self.test_vin, 'firmware_modules': self.updated_firmware})
        self.assertTrue(len(vin_firmware_versions) > 0)

    # test errors
    def test_firmware_version_vin_set_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            firmware_functions.firmware_version_vin_set({'vin': None, 'firmware_modules': self.updated_firmware})

    def test_firmware_version_vin_set_error_input_null_firmware_modules(self):
        with self.assertRaises(ArcimotoArgumentError):
            firmware_functions.firmware_version_vin_set({'vin': self.test_vin, 'firmware_modules': None})

    def test_firmware_version_vin_set_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            firmware_functions.firmware_version_vin_set({'vin': 1, 'firmware_modules': self.updated_firmware})

    def test_firmware_version_vin_set_error_input_invalid_type_firmware_modules(self):
        with self.assertRaises(ArcimotoArgumentError):
            firmware_functions.firmware_version_vin_set({'vin': self.test_vin, 'firmware_modules': 'not a dictionary'})

    def test_firmware_version_vin_set_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            firmware_functions.firmware_version_vin_set({'vin': self.test_vin, 'firmware_modules': self.updated_firmware}, False)


@arcimoto.runtime.handler
def test_firmware_version_vin_set():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(FirmwareVersionVinSetTestCase)
    ))


lambda_handler = test_firmware_version_vin_set
