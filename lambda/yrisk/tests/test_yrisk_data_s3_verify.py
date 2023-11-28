import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import yrisk_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class YriskDataS3VerifyTestCase(unittest.TestCase):

    s3_local_bucket = 'arcimoto-yrisk'
    s3_yrisk_bucket = 'y-risk-client-exposure-data'

    def test_yrisk_data_s3_verify_success_local(self):
        self.assertIsInstance(yrisk_functions.data_s3_verify(self.s3_local_bucket), dict)

    # test errors
    def test_yrisk_data_s3_verify_error_input_null_s3_bucket(self):
        with self.assertRaises(ArcimotoArgumentError):
            yrisk_functions.data_s3_verify(None)

    def test_yrisk_data_s3_verify_error_input_empty_s3_bucket(self):
        with self.assertRaises(ArcimotoArgumentError):
            yrisk_functions.data_s3_verify('')

    def test_yrisk_data_s3_verify_error_input_invalid_type_s3_bucket(self):
        with self.assertRaises(ArcimotoArgumentError):
            yrisk_functions.data_s3_verify(1)


@arcimoto.runtime.handler
def test_yrisk_data_s3_verify():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(YriskDataS3VerifyTestCase)
    ))


lambda_handler = test_yrisk_data_s3_verify
