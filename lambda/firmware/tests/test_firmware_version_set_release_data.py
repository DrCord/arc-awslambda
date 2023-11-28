import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import firmware_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class FirmwareVersionSetReleaseDataTestCase(unittest.TestCase):

    firmware_versions_release_data = None

    @classmethod
    def setUpClass(cls):
        cls.firmware_versions_release_data = firmware_functions.firmware_version_get_release_data('deployedfirmware')

    def test_firmware_version_set_release_data_success(self):
        updated_firmware = firmware_functions.firmware_version_set_release_data(self.firmware_versions_release_data)
        self.assertTrue(len(updated_firmware) > 0)

    # test errors
    def test_firmware_version_set_release_data_error_input_invalid_type_firmware(self):
        with self.assertRaises(ArcimotoArgumentError):
            firmware_functions.firmware_version_set_release_data({'firmware': 'not a dictionary'})


@arcimoto.runtime.handler
def test_firmware_version_set_release_data():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(FirmwareVersionSetReleaseDataTestCase)
    ))


lambda_handler = test_firmware_version_set_release_data
