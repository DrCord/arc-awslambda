import logging
import unittest
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MessageBrokerTestCase(unittest.TestCase):

    vin = arcimoto.tests.uuid_vin_get()
    args = {
        'Records': [
            {
                'body': {
                    'severity': 'CRITICAL',
                    'message': 'Unit test CRITICAL level test message',
                    'source_type': 'lambda',
                    'source': 'test_message_broker',
                    'data': {
                        'note': {
                            'object_type': 'Vehicle',
                            'object_id': vin,
                            'author': 'UNIT_TEST',
                            'content': 'created by message_broker unit test CRITICAL message',
                            'tags': [
                                'service',
                                'firmware',
                                'delivery',
                                'manufacturing',
                                'quality',
                                'debugging'
                            ]
                        }
                    }
                }
            },
            {
                'body': {
                    'severity': 'ERROR',
                    'message': 'Unit test ERROR level test message',
                    'source_type': 'lambda',
                    'source': 'test_message_broker',
                    'data': {
                        'note': {
                            'object_type': 'Vehicle',
                            'object_id': vin,
                            'author': 'UNIT_TEST',
                            'content': 'created by message_broker unit test CRITICAL message',
                            'tags': [
                                'service',
                                'firmware',
                                'delivery',
                                'manufacturing',
                                'quality',
                                'debugging'
                            ]
                        }
                    }
                }
            },
            {
                'body': {
                    'severity': 'WARNING',
                    'message': 'Unit test WARNING level test message',
                    'source_type': 'lambda',
                    'source': 'test_message_broker',
                    'data': {
                        'note': {
                            'object_type': 'Vehicle',
                            'object_id': vin,
                            'author': 'UNIT_TEST',
                            'content': 'created by message_broker unit test WARNING message',
                            'tags': [
                                'service',
                                'firmware',
                                'delivery',
                                'manufacturing',
                                'quality',
                                'debugging'
                            ]
                        }
                    }
                }
            },
            {
                'body': {
                    'severity': 'INFO',
                    'message': 'Unit test INFO level test message',
                    'source_type': 'lambda',
                    'source': 'test_message_broker',
                    'data': {
                        'note': {
                            'object_type': 'Vehicle',
                            'object_id': vin,
                            'author': 'UNIT_TEST',
                            'content': 'created by message_broker unit test INFO message',
                            'tags': [
                                'service',
                                'firmware',
                                'delivery',
                                'manufacturing',
                                'quality',
                                'debugging'
                            ]
                        }
                    }
                }
            }
        ]
    }

    def test_message_broker_success_with_notes(self):
        args = copy.deepcopy(self.args)
        self.assertIsInstance(arcimoto.runtime.invoke_lambda('message_broker', args), dict)

    def test_message_broker_success_slack_notifications_channel_default(self):
        args = copy.deepcopy(self.args)
        for record in args.get('Records'):
            del record['body']['data']['note']
        self.assertIsInstance(arcimoto.runtime.invoke_lambda('message_broker', args), dict)

    def test_message_broker_success_slack_notifications_channel_firmware(self):
        args = copy.deepcopy(self.args)
        for record in args.get('Records'):
            del record['body']['data']['note']
            record['body']['channel'] = 'firmware'
        self.assertIsInstance(arcimoto.runtime.invoke_lambda('message_broker', args), dict)

    def test_message_broker_success_slack_notifications_channel_manufacturing(self):
        args = copy.deepcopy(self.args)
        for record in args.get('Records'):
            del record['body']['data']['note']
            record['body']['channel'] = 'manufacturing'
        self.assertIsInstance(arcimoto.runtime.invoke_lambda('message_broker', args), dict)

    def test_message_broker_success_slack_notifications_channel_network(self):
        args = copy.deepcopy(self.args)
        for record in args.get('Records'):
            del record['body']['data']['note']
            record['body']['channel'] = 'network'
        self.assertIsInstance(arcimoto.runtime.invoke_lambda('message_broker', args), dict)

    def test_message_broker_success_slack_notifications_channel_orders(self):
        args = copy.deepcopy(self.args)
        for record in args.get('Records'):
            del record['body']['data']['note']
            record['body']['channel'] = 'orders'
        self.assertIsInstance(arcimoto.runtime.invoke_lambda('message_broker', args), dict)

    def test_message_broker_success_slack_notifications_channel_reef(self):
        args = copy.deepcopy(self.args)
        for record in args.get('Records'):
            del record['body']['data']['note']
            record['body']['channel'] = 'reef'
        self.assertIsInstance(arcimoto.runtime.invoke_lambda('message_broker', args), dict)

    def test_message_broker_success_slack_notifications_channel_replicate(self):
        args = copy.deepcopy(self.args)
        for record in args.get('Records'):
            del record['body']['data']['note']
            record['body']['channel'] = 'replicate'
        self.assertIsInstance(arcimoto.runtime.invoke_lambda('message_broker', args), dict)

    def test_message_broker_success_slack_notifications_channel_service(self):
        args = copy.deepcopy(self.args)
        for record in args.get('Records'):
            del record['body']['data']['note']
            record['body']['channel'] = 'service'
        self.assertIsInstance(arcimoto.runtime.invoke_lambda('message_broker', args), dict)

    def test_message_broker_success_slack_notifications_channel_telemetry(self):
        args = copy.deepcopy(self.args)
        for record in args.get('Records'):
            del record['body']['data']['note']
            record['body']['channel'] = 'telemetry'
        self.assertIsInstance(arcimoto.runtime.invoke_lambda('message_broker', args), dict)

    def test_message_broker_success_slack_notifications_channel_yrisk(self):
        args = copy.deepcopy(self.args)
        for record in args.get('Records'):
            del record['body']['data']['note']
            record['body']['channel'] = 'yrisk'
        self.assertIsInstance(arcimoto.runtime.invoke_lambda('message_broker', args), dict)

    def test_message_broker_success_slack_notifications_records(self):
        args = {}
        args['records'] = copy.deepcopy(self.args['Records'])
        for record in args.get('records'):
            del record['body']['data']['note']
        self.assertIsInstance(arcimoto.runtime.invoke_lambda('message_broker', args), dict)

    # test errors
    def test_message_broker_error_input_null_Records(self):
        with self.assertRaises(ArcimotoArgumentError):
            arcimoto.runtime.invoke_lambda('message_broker', {'Records': None})

    def test_message_broker_error_input_invalid_type_Records(self):
        with self.assertRaises(ArcimotoArgumentError):
            arcimoto.runtime.invoke_lambda('message_broker', {'Records': 'not a list'})

    def test_message_broker_error_input_invalid_empty_Records(self):
        with self.assertRaises(ArcimotoArgumentError):
            arcimoto.runtime.invoke_lambda('message_broker', {'Records': []})

    def test_message_broker_error_input_null_records(self):
        with self.assertRaises(ArcimotoArgumentError):
            arcimoto.runtime.invoke_lambda('message_broker', {'records': None})

    def test_message_broker_error_input_invalid_type_records(self):
        with self.assertRaises(ArcimotoArgumentError):
            arcimoto.runtime.invoke_lambda('message_broker', {'records': 'not a list'})

    def test_message_broker_error_input_invalid_empty_records(self):
        with self.assertRaises(ArcimotoArgumentError):
            arcimoto.runtime.invoke_lambda('message_broker', {'records': []})


@arcimoto.runtime.handler
def test_message_broker():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(MessageBrokerTestCase)
    ))


lambda_handler = test_message_broker
