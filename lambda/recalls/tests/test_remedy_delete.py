import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import recall_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RecallRemedyDeleteTestCase(unittest.TestCase):

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
        if cls.recall_id is not None:
            recall_functions.recall_delete(cls.recall_id)

    def test_remedy_delete_success(self):
        recall_functions.remedy_delete({'remedy_id': self.remedy_id})
        recall = recall_functions.recall_get(self.recall_id)
        self.assertFalse(recall.get('remedy_id', None))

    # test errors
    def test_remedy_delete_error_input_null_remedy_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_delete({'remedy_id': None})

    def test_remedy_delete_error_input_invalid_type_remedy_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_delete({'remedy_id': 'not an integer'})

    def test_remedy_delete_error_input_invalid_remedy_id_must_be_positive_integer(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_delete({'remedy_id': -1})

    def test_remedy_delete_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            recall_functions.remedy_delete({'remedy_id': self.remedy_id}, False)


@arcimoto.runtime.handler
def test_remedy_delete():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RecallRemedyDeleteTestCase)
    ))


lambda_handler = test_remedy_delete
