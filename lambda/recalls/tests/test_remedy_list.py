import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import recall_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RecallRemedyListTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.recall_id = recall_functions.recall_create()
        args = {
            'recall_id': cls.recall_id,
            'description': 'Created by unit test'
        }
        cls.remedy_id = recall_functions.remedy_create(args)

    @classmethod
    def tearDownClass(cls):
        if cls.remedy_id is not None:
            recall_functions.remedy_delete({'remedy_id': cls.remedy_id})
        if cls.recall_id is not None:
            recall_functions.recall_delete(cls.recall_id)

    def test_remedy_list_success(self):
        self.assertTrue(len(recall_functions.remedy_list()) > 0)

    # test errors
    def test_remedy_list_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            recall_functions.remedy_list(False)


@arcimoto.runtime.handler
def test_remedy_list():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RecallRemedyListTestCase)
    ))


lambda_handler = test_remedy_list
