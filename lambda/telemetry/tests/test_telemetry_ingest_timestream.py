import logging
import unittest
from datetime import datetime
import random
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import telemetry_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TelemetryIngestTimestreamTestCase(unittest.TestCase):

    vin = None
    args =  {
        'Records': [
            {
                'body': {
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
            }
        ]
    }

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        cls.args['Records'][0]['body']['vin'] = cls.vin

    def test_telemetry_ingest_timestream_success(self):
        args = copy.deepcopy(self.args)
        self.assertFalse(telemetry_functions.telemetry_ingest_timestream(args))

    # test errors
    def test_telemetry_ingest_timestream_error_input_null_vin(self):
        args = copy.deepcopy(self.args)
        args['Records'][0]['body']['vin'] = None
        with self.assertRaises(ArcimotoArgumentError):
            telemetry_functions.telemetry_ingest_timestream(args)

    def test_telemetry_ingest_timestream_error_input_null_data(self):
        args = copy.deepcopy(self.args)
        args['Records'][0]['body']['data'] = None
        with self.assertRaises(ArcimotoArgumentError):
            telemetry_functions.telemetry_ingest_timestream(args)


@arcimoto.runtime.handler
def test_telemetry_ingest_timestream():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(TelemetryIngestTimestreamTestCase)
    ))


lambda_handler = test_telemetry_ingest_timestream
