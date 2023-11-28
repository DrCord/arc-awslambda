import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import utility_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PrintLabelRequestTestCase(unittest.TestCase):

    args = {
        'printer': 'ZD620',
        'remote_filename': 'c:\\labels\\delivery_sticker.nlbl',
        'label_variables': {
            'factory_pin': '123456',
            'qr_code': '{\"vin\": \"DEV-CORDFUV\"}\n====SIGNATURE====\nhqM+Fzq1kv+JuJIYLaAwDKPRXQJ4YlJBww+OoaaxmU5WBXHrqcrj5G0+GdHBm6rDa24G2A1r7L0+I+/94EVV9w=='
        }
    }

    def test_print_label_request_success(self):
        self.assertIsInstance(utility_functions.print_label(self.args), dict)

    # test errors
    def test_print_label_request_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            utility_functions.print_label(self.args, False)


@arcimoto.runtime.handler
def test_print_label_request():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(PrintLabelRequestTestCase)
    ))


lambda_handler = test_print_label_request
