from copy import deepcopy
import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import unit_test_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UnitTestNotifyTestCase(unittest.TestCase):

    args = {
        'event': 'Unit tests: unit_test_notify running',
        'message_addendum': 'running unit tests is great!',
        'event_data': {
            'prop1': 'unit test fake data',
            'prop2': 'more unit test fake data'
        },
        'severity': 'INFO'
    }

    def test_unit_test_notify_success(self):
        self.assertIsInstance(unit_test_functions.unit_test_notify(self.args), dict)

    # test errors
    def test_unit_test_notify_error_input_no_event(self):
        args = deepcopy(self.args)
        del args['event']
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_notify(args)

    def test_unit_test_notify_error_input_null_event(self):
        args = deepcopy(self.args)
        args['event'] = None
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_notify(args)

    def test_unit_test_notify_error_input_invalid_type_event(self):
        args = deepcopy(self.args)
        args['event'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_notify(args)

    def test_unit_test_notify_error_input_invalid_type_message_addendum(self):
        args = deepcopy(self.args)
        args['message_addendum'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_notify(args)

    def test_unit_test_notify_error_input_invalid_type_event_data(self):
        args = deepcopy(self.args)
        args['event_data'] = 'not a dictionary'
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_notify(args)

    def test_unit_test_notify_error_input_invalid_type_severity(self):
        args = deepcopy(self.args)
        args['severity'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_notify(args)

    def test_unit_test_notify_error_input_disallowed_severity(self):
        args = deepcopy(self.args)
        args['severity'] = 'not an allowed value'
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_notify(args)


@arcimoto.runtime.handler
def test_unit_test_notify():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UnitTestNotifyTestCase)
    ))


lambda_handler = test_unit_test_notify
