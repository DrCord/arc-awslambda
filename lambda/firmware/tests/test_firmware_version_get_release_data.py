import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import firmware_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class FirmwareVersionGetReleaseDataTestCase(unittest.TestCase):

    def test_firmware_version_get_release_data_success(self):
        response = firmware_functions.firmware_version_get_release_data('deployedfirmware')
        firmware_versions_release_data = response.get('firmware', {})
        for firmware_version_data in firmware_versions_release_data:
            self.assertTrue(firmware_versions_release_data[firmware_version_data].get('hash', '') is not '')

    # test errors
    def test_firmware_version_get_release_data_error_input_null_repo(self):
        with self.assertRaises(ArcimotoArgumentError):
            firmware_functions.firmware_version_get_release_data(None)

    def test_firmware_version_get_release_data_error_input_invalid_type_repo(self):
        with self.assertRaises(ArcimotoArgumentError):
            firmware_functions.firmware_version_get_release_data(1)


@arcimoto.runtime.handler
def test_firmware_version_get_release_data():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(FirmwareVersionGetReleaseDataTestCase)
    ))


lambda_handler = test_firmware_version_get_release_data
