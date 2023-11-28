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


class BackfillS3LoadFileTestCase(unittest.TestCase):

    BUCKET_NAME = 'arcimoto-backfill'
    file_content = 'test_backfill_s3_load_file unit test content'.encode('utf-8')
    args = {
        'file_name': 'unit_test_file_to_load.txt',
        'file_length': len(file_content)
    }

    @classmethod
    def setUpClass(cls):
        # create a tiny file and upload for load testing
        s3 = boto3.resource('s3')
        try:
            object = s3.Object(cls.BUCKET_NAME, cls.args['file_name'])
            response = object.put(Body=cls.file_content)
        except ClientError:
            logger.exception('Could not upload object to bucket.')
            raise
        except Exception as e:
            raise ArcimotoException(e)

    @classmethod
    def tearDownClass(cls):
        backfill_functions.s3_delete_file(cls.args)

    def test_backfill_s3_load_file_success(self):
        args = copy.deepcopy(self.args)
        self.assertIsInstance(backfill_functions.s3_load_file(args), dict)

    # test errors
    def test_backfill_s3_load_file_error_input_null_file_name(self):
        args = copy.deepcopy(self.args)
        args['file_name'] = None
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.s3_load_file(args)

    def test_backfill_s3_load_file_error_input_null_file_length(self):
        args = copy.deepcopy(self.args)
        args['file_length'] = None
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.s3_load_file(args)

    def test_backfill_s3_load_file_error_input_invalid_type_file_name(self):
        args = copy.deepcopy(self.args)
        args['file_name'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.s3_load_file(args)

    def test_backfill_s3_load_file_error_input_invalid_type_file_length(self):
        args = copy.deepcopy(self.args)
        args['file_length'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.s3_load_file(args)

    def test_backfill_s3_load_file_error_input_invalid_type_next_read_byte(self):
        args = copy.deepcopy(self.args)
        args['next_read_byte'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.s3_load_file(args)


@arcimoto.runtime.handler
def test_backfill_s3_load_file():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(BackfillS3LoadFileTestCase)
    ))


lambda_handler = test_backfill_s3_load_file
