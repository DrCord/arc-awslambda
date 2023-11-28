import logging
import unittest
import copy
import uuid
import json
import boto3
from botocore.exceptions import ClientError

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import backfill_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BackfillStateMachineStartTestCase(unittest.TestCase):

    BUCKET_NAME = 'arcimoto-backfill'
    vin = None
    telemetry_atom = {
        "epsu_current": 0.05660725,
        "bms_pack_current": 478,
        "speed": 32.2,
        "odometer": 1911.0,
        "timestamp": "2020-12-08T21:00:06.10Z",
        "steering_angle": 62024,
        "gps_position": "34.07751,-118.4106"
    }
    file_content = json.dumps(telemetry_atom).encode('utf-8')
    args = {
        'vin': None,
        'file_name': 'unit_test_file_state_machine_start.txt',
        'file_length': len(file_content)
    }

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        cls.args['vin'] = cls.vin
        # create a tiny file and upload for state machine to use
        s3 = boto3.resource('s3')
        try:
            object = s3.Object(cls.BUCKET_NAME, cls.args['file_name'])
            response = object.put(Body=cls.file_content)
        except ClientError:
            logger.exception('Could not upload object to bucket.')
            raise
        except Exception as e:
            raise ArcimotoException(e)

    def test_backfill_state_machine_start_success(self):
        args = copy.deepcopy(self.args)
        self.assertIsInstance(backfill_functions.state_machine_start(args), dict)

    # test errors
    def test_backfill_state_machine_start_error_input_null_vin(self):
        args = copy.deepcopy(self.args)
        args['vin'] = None
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.state_machine_start(args)

    def test_backfill_state_machine_start_error_input_null_file_name(self):
        args = copy.deepcopy(self.args)
        args['file_name'] = None
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.state_machine_start(args)

    def test_backfill_state_machine_start_error_input_null_file_length(self):
        args = copy.deepcopy(self.args)
        args['file_length'] = None
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.state_machine_start(args)

    def test_backfill_state_machine_start_error_input_invalid_type_vin(self):
        args = copy.deepcopy(self.args)
        args['vin'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.state_machine_start(args)

    def test_backfill_state_machine_start_error_input_invalid_type_file_name(self):
        args = copy.deepcopy(self.args)
        args['file_name'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.state_machine_start(args)

    def test_backfill_state_machine_start_error_input_invalid_type_file_length(self):
        args = copy.deepcopy(self.args)
        args['file_length'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.state_machine_start(args)


@arcimoto.runtime.handler
def test_backfill_state_machine_start():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(BackfillStateMachineStartTestCase)
    ))


lambda_handler = test_backfill_state_machine_start
