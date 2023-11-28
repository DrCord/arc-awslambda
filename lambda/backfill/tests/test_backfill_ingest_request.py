import logging
import unittest
from datetime import datetime
import random
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import backfill_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BackfillIngestRequestTestCase(unittest.TestCase):

    vin = None
    args = {
        'vin': None,
        'data': [
            {
                'ambient_temp': random.randint(1, 101),
                'timestamp': str(datetime.now().time()) + ' UTC'
            },
            {
                'speed': random.randint(1, 101),
                'timestamp': str(datetime.now().time()) + ' UTC'
            }
        ],
        'env_prefix': True
    }

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)
        cls.args['vin'] = cls.vin

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_backfill_ingest_request_success(self):
        args = copy.deepcopy(self.args)
        self.assertFalse(backfill_functions.ingest_request(args))

    # test errors
    def test_backfill_ingest_request_error_input_null_vin(self):
        args = copy.deepcopy(self.args)
        args['vin'] = None
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.ingest_request(args)

    def test_backfill_ingest_request_error_input_null_data(self):
        args = copy.deepcopy(self.args)
        args['data'] = None
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.ingest_request(args)

    def test_backfill_ingest_request_error_input_invalid_type_vin(self):
        args = copy.deepcopy(self.args)
        args['vin'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.ingest_request(args)

    def test_backfill_ingest_request_error_input_invalid_type_data(self):
        args = copy.deepcopy(self.args)
        args['data'] = 'not a list'
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.ingest_request(args)

    def test_backfill_ingest_request_error_input_empty_data(self):
        args = copy.deepcopy(self.args)
        args['data'] = []
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.ingest_request(args)


@arcimoto.runtime.handler
def test_backfill_ingest_request():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(BackfillIngestRequestTestCase)
    ))


lambda_handler = test_backfill_ingest_request
