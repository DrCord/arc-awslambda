import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import recall_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RecallDeleteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.recall_id = recall_functions.recall_create()

    def test_recall_delete_success(self):
        recall_functions.recall_delete(self.recall_id)
        recall = recall_functions.recall_get(self.recall_id)
        self.assertTrue(recall.get('status', None) == 'deleted')

    # test errors
    def test_recall_delete_error_input_null_recall_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_delete(None)

    def test_recall_delete_error_input_invalid_type_recall_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_delete('not an integer')

    def test_recall_delete_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            recall_functions.recall_delete(self.recall_id, False)


@arcimoto.runtime.handler
def test_recall_delete():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RecallDeleteTestCase)
    ))


lambda_handler = test_recall_delete
