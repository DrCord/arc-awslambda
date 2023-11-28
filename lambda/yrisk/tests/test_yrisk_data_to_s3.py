import logging
import unittest
from datetime import datetime


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import yrisk_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class YriskDataToS3TestCase(unittest.TestCase):

    s3_local_bucket = 'arcimoto-yrisk'
    s3_yrisk_bucket = 'y-risk-client-exposure-data'
    json_data = {
        'arcimoto-unit-test-generated': arcimoto.db.datetime_record_output(datetime.now())
    }

    def test_yrisk_data_to_s3_success_local(self):
        self.assertIsInstance(yrisk_functions.data_to_s3(self.s3_local_bucket, self.json_data), dict)

    def test_yrisk_data_to_s3_success_yrisk(self):
        self.assertIsInstance(yrisk_functions.data_to_s3(self.s3_yrisk_bucket, self.json_data), dict)

    # test errors
    def test_yrisk_data_to_s3_error_input_null_s3_bucket(self):
        with self.assertRaises(ArcimotoArgumentError):
            yrisk_functions.data_to_s3(None, self.json_data)

    def test_yrisk_data_to_s3_error_input_null_json_data(self):
        with self.assertRaises(ArcimotoArgumentError):
            yrisk_functions.data_to_s3(self.s3_local_bucket, None)

    def test_yrisk_data_to_s3_error_input_empty_s3_bucket(self):
        with self.assertRaises(ArcimotoArgumentError):
            yrisk_functions.data_to_s3('', self.json_data)

    def test_yrisk_data_to_s3_error_input_invalid_type_s3_bucket(self):
        with self.assertRaises(ArcimotoArgumentError):
            yrisk_functions.data_to_s3(1, self.json_data)

    def test_yrisk_data_to_s3_error_input_invalid_type_json_data(self):
        with self.assertRaises(ArcimotoArgumentError):
            yrisk_functions.data_to_s3(self.s3_local_bucket, 'not a dictionary')


@arcimoto.runtime.handler
def test_yrisk_data_to_s3():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(YriskDataToS3TestCase)
    ))


lambda_handler = test_yrisk_data_to_s3
