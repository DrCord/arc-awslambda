import logging
import unittest
import datetime

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import recall_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RecallSetUpdatedTestCase(unittest.TestCase):

    def test_recall_set_updated_success_input_null(self):
        self.assertIsInstance(recall_functions.recall_set_updated(), dict)

    def test_recall_set_updated_success_input_updated(self):
        self.assertIsInstance(recall_functions.recall_set_updated(str(datetime.datetime.utcnow())), dict)

    # test errors
    def test_recall_set_updated_error_input_invalid_type_updated(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_set_updated(1)

    def test_recall_set_updated_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            recall_functions.recall_set_updated(None, False)


@arcimoto.runtime.handler
def test_recall_set_updated():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RecallSetUpdatedTestCase)
    ))


lambda_handler = test_recall_set_updated
