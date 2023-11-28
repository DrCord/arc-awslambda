import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import firmware_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class FirmwareVersionVinGetTestCase(unittest.TestCase):

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.test_vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.test_vin)
        firmware_versions_release_data_response = firmware_functions.firmware_version_get_release_data('deployedfirmware')
        updated_firmware = firmware_functions.firmware_version_set_release_data(firmware_versions_release_data_response)
        firmware_functions.firmware_version_vin_set({'vin': cls.test_vin, 'firmware_modules': updated_firmware})

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.test_vin)

    def test_firmware_version_vin_get_success(self):
        vin_firmware_versions = firmware_functions.firmware_version_vin_get(self.test_vin)
        self.assertTrue(len(vin_firmware_versions) > 0)

    # test errors
    def test_firmware_version_vin_get_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            firmware_functions.firmware_version_vin_get(None)

    def test_firmware_version_vin_get_error_vin_does_not_exist(self):
        with self.assertRaises(ArcimotoArgumentError):
            firmware_functions.firmware_version_vin_get(self.vin_invalid)

    def test_firmware_version_vin_get_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            firmware_functions.firmware_version_vin_get(1)

    def test_firmware_version_vin_get_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            firmware_functions.firmware_version_vin_get(self.test_vin, False)


@arcimoto.runtime.handler
def test_firmware_version_vin_get():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(FirmwareVersionVinGetTestCase)
    ))


lambda_handler = test_firmware_version_vin_get
