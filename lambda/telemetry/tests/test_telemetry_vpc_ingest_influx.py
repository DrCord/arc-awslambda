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


class TelemetryVpcIngestInfluxTestCase(unittest.TestCase):

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
        arcimoto.tests.vehicle_create(cls.vin)
        cls.args['Records'][0]['body']['vin'] = cls.vin

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_telemetry_vpc_ingest_influx_success(self):
        args = copy.deepcopy(self.args)
        self.assertFalse(telemetry_functions.telemetry_vpc_ingest_influx(args))

    # test errors
    def test_telemetry_vpc_ingest_influx_error_input_null_vin(self):
        args = copy.deepcopy(self.args)
        args['Records'][0]['body']['vin'] = None
        with self.assertRaises(ArcimotoArgumentError):
            telemetry_functions.telemetry_vpc_ingest_influx(args)

    def test_telemetry_vpc_ingest_influx_error_input_null_data(self):
        args = copy.deepcopy(self.args)
        args['Records'][0]['body']['data'] = None
        with self.assertRaises(ArcimotoArgumentError):
            telemetry_functions.telemetry_vpc_ingest_influx(args)

    def test_telemetry_vpc_ingest_influx_error_empty_data(self):
        args = copy.deepcopy(self.args)
        args['Records'][0]['body']['data'] = [{}]
        with self.assertRaises(ArcimotoTelemetryAlertException):
            telemetry_functions.telemetry_vpc_ingest_influx(args)


@arcimoto.runtime.handler
def test_telemetry_vpc_ingest_influx():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(TelemetryVpcIngestInfluxTestCase)
    ))


lambda_handler = test_telemetry_vpc_ingest_influx