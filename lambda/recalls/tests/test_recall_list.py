import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import recall_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RecallListTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.recall_id = recall_functions.recall_create()
        cls.recall_list_original_len = len(recall_functions.recall_list())

    def test_recall_list_success_input_null(self):
        self.assertTrue(self.recall_list_original_len > 0)

    def test_recall_list_success_input_get_deleted_recalls(self):
        if self.recall_id is not None:
            recall_functions.recall_delete(self.recall_id)
        recall_list_incl_deleted_len = len(recall_functions.recall_list(True))
        self.assertTrue(recall_list_incl_deleted_len > self.recall_list_original_len)

    # test errors
    def test_recall_list_error_input_invalid_type_get_deleted_recalls(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_list('not a boolean')

    def test_recall_list_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            recall_functions.recall_list(False, False)


@arcimoto.runtime.handler
def test_recall_list():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RecallListTestCase)
    ))


lambda_handler = test_recall_list
