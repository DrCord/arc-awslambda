import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import recall_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RecallGetTestCase(unittest.TestCase):

    @property
    def recall_id_invalid(self):
        return recall_functions.recalls_get_highest_id() + 1

    @classmethod
    def setUpClass(cls):
        cls.recall_id = recall_functions.recall_create()

    @classmethod
    def tearDownClass(cls):
        if cls.recall_id is not None:
            recall_functions.recall_delete(cls.recall_id)

    def test_recall_get_success_input_recall_id(self):
        self.assertIsInstance(recall_functions.recall_get(self.recall_id), dict)

    def test_recall_get_success_input_get_additional_data(self):
        recall = recall_functions.recall_get(self.recall_id, True)
        self.assertIsInstance(recall, dict)
        self.assertIsInstance(recall['vehicles'], list)

    # test errors
    def test_recall_get_error_invalid_recall_id_does_not_exist(self):
        with self.assertRaises(ArcimotoException):
            recall_functions.recall_get(self.recall_id_invalid)

    def test_recall_get_error_input_invalid_recall_id_must_be_positive_integer(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_get(-1)

    def test_recall_get_error_input_invalid_type_recall_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_get('not an integer')

    def test_recall_get_error_input_invalid_type_get_additional_data(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_get(self.recall_id, 'not a boolean')

    def test_recall_get_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            recall_functions.recall_get(self.recall_id, False, False)


@arcimoto.runtime.handler
def test_recall_get():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RecallGetTestCase)
    ))


lambda_handler = test_recall_get
