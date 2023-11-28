import logging
import unittest
import copy
import uuid

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import backfill_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BackfillNotifyCompleteTestCase(unittest.TestCase):

    vin = None
    args = {
        'vin': None,
        'recipient': 'unittest+' + uuid.uuid4().hex + '@arcimoto.com',
        'file_name': 'not-a-real-file.test'
    }

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        cls.args['vin'] = cls.vin

    def test_backfill_notify_complete_success(self):
        args = copy.deepcopy(self.args)
        self.assertIsInstance(backfill_functions.notify_complete(args), dict)

    # test errors
    def test_backfill_notify_complete_error_input_null_vin(self):
        args = copy.deepcopy(self.args)
        args['vin'] = None
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.notify_complete(args)

    def test_backfill_notify_complete_error_input_null_recipient(self):
        args = copy.deepcopy(self.args)
        args['recipient'] = None
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.notify_complete(args)

    def test_backfill_notify_complete_error_input_null_file_name(self):
        args = copy.deepcopy(self.args)
        args['file_name'] = None
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.notify_complete(args)

    def test_backfill_notify_complete_error_input_invalid_type_vin(self):
        args = copy.deepcopy(self.args)
        args['vin'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.notify_complete(args)

    def test_backfill_notify_complete_error_input_invalid_type_recipient(self):
        args = copy.deepcopy(self.args)
        args['recipient'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.notify_complete(args)

    def test_backfill_notify_complete_error_input_invalid_type_file_name(self):
        args = copy.deepcopy(self.args)
        args['file_name'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            backfill_functions.notify_complete(args)


@arcimoto.runtime.handler
def test_backfill_notify_complete():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(BackfillNotifyCompleteTestCase)
    ))


lambda_handler = test_backfill_notify_complete
