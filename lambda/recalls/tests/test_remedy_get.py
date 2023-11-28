import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import recall_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RecallRemedyGetTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.recall_id = recall_functions.recall_create()
        args = {
            'recall_id': cls.recall_id,
            'description': 'Created by unit test script'
        }
        cls.remedy_id = recall_functions.remedy_create(args)

    @classmethod
    def tearDownClass(cls):
        if cls.remedy_id is not None:
            recall_functions.remedy_delete({'remedy_id': cls.remedy_id})
        if cls.recall_id is not None:
            recall_functions.recall_delete(cls.recall_id)

    def test_remedy_get_success(self):
        self.assertIsInstance(recall_functions.remedy_get(self.remedy_id), dict)

    # test errors
    def test_remedy_get_error_input_null_remedy_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_get(None)

    def test_remedy_get_error_input_remedy_id_must_be_positive_integer(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_get(-1)

    def test_remedy_get_error_input_invalid_type_remedy_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_get('not an integer')

    def test_remedy_get_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            recall_functions.remedy_get(self.remedy_id, False)


@arcimoto.runtime.handler
def test_remedy_get():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RecallRemedyGetTestCase)
    ))


lambda_handler = test_remedy_get
