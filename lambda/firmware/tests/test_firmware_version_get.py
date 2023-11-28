import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import firmware_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class FirmwareVersionGetTestCase(unittest.TestCase):

    firmware_modules_input = {
        'firmware_modules_input': {
            'BMS Firmware': None,
            'Comm Firmware': None
        }
    }

    def test_firmware_version_get_success_no_input(self):
        self.assertTrue(len(firmware_functions.firmware_version_get({})) > 0)

    def test_firmware_version_get_success_input(self):
        firmware_versions = firmware_functions.firmware_version_get(self.firmware_modules_input)
        self.assertIsNotNone(firmware_versions.get('BMS Firmware', None))
        self.assertIsNotNone(firmware_versions.get('Comm Firmware', None))
        self.assertTrue(len(firmware_versions) == 2)

    # test errors
    def test_firmware_version_get_error_input_invalid_type_firmware_modules_input(self):
        with self.assertRaises(ArcimotoArgumentError):
            firmware_functions.firmware_version_get({'firmware_modules_input': 'not a dictionary'})

    def test_firmware_version_get_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            firmware_functions.firmware_version_get(self.firmware_modules_input, False)


@arcimoto.runtime.handler
def test_firmware_version_get():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(FirmwareVersionGetTestCase)
    ))


lambda_handler = test_firmware_version_get
