import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import recall_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RecallGetUpdatedTestCase(unittest.TestCase):

    def test_recall_get_updated_success_input_first(self):
        self.assertIsInstance(recall_functions.recall_get_updated(None, True, False), dict)

    def test_recall_get_updated_success_input_last(self):
        self.assertIsInstance(recall_functions.recall_get_updated(None, False, True), dict)

    def test_recall_get_updated_success_input_id(self):
        self.assertIsInstance(recall_functions.recall_get_updated(0), dict)

    # test errors
    def test_recall_get_updated_error_input_first_and_last_mutually_exclusive(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_get_updated(None, True, True)

    def test_recall_get_updated_error_input_id_required_if_first_and_last_none(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_get_updated(None, False, False)


@arcimoto.runtime.handler
def test_recall_get_updated():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RecallGetUpdatedTestCase)
    ))


lambda_handler = test_recall_get_updated
