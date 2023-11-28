import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import firmware_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class FirmwareGetCommitInfoTestCase(unittest.TestCase):

    def test_firmware_get_commit_info_success(self):
        firmware_commit_info = firmware_functions.firmware_get_commit_info({'repo': 'deployedfirmware'})
        self.assertIsNotNone(firmware_commit_info.get('hash', None))

    # test errors
    def test_firmware_get_commit_info_error_input_null_repo(self):
        with self.assertRaises(ArcimotoArgumentError):
            firmware_functions.firmware_get_commit_info({'repo': None})

    def test_firmware_get_commit_info_error_input_invalid_type_repo(self):
        with self.assertRaises(ArcimotoArgumentError):
            firmware_functions.firmware_get_commit_info({'repo': 1})

    def test_firmware_get_commit_info_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            firmware_functions.firmware_get_commit_info({'repo': 'deployedfirmware'}, False)


@arcimoto.runtime.handler
def test_firmware_get_commit_info():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(FirmwareGetCommitInfoTestCase)
    ))


lambda_handler = test_firmware_get_commit_info
