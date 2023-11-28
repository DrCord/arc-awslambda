import logging
import unittest
import copy
import boto3
from botocore.exceptions import ClientError

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import backfill_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BackfillS3PresignedUrlGenerateTestCase(unittest.TestCase):

    BUCKET_NAME = 'arcimoto-backfill'
    args = {
        'file_name': 'unit_test_file_s3_presigned_url_generate.txt'
    }

    def test_backfill_s3_presigned_url_generate_success(self):
        args = copy.deepcopy(self.args)
        self.assertIsInstance(backfill_functions.s3_presigned_url_generate(args), dict)

    # test errors
    def test_backfill_s3_presigned_url_generate_error_input_null_file_name(self):
        args = copy.deepcopy(self.args)
        args['file_name'] = None
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.s3_presigned_url_generate(args)

    def test_backfill_s3_presigned_url_generate_error_input_invalid_type_file_name(self):
        args = copy.deepcopy(self.args)
        args['file_name'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.s3_presigned_url_generate(args)


@arcimoto.runtime.handler
def test_backfill_s3_presigned_url_generate():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(BackfillS3PresignedUrlGenerateTestCase)
    ))


lambda_handler = test_backfill_s3_presigned_url_generate
