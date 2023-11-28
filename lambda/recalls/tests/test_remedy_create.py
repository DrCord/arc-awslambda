import logging
import unittest
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import recall_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RecallRemedyCreateTestCase(unittest.TestCase):

    recall_id = None
    args = {
        'recall_id': None,
        'description': 'Created by unit test script'
    }

    @property
    def recall_id_invalid(self):
        return recall_functions.recalls_get_highest_id() + 1

    @classmethod
    def setUpClass(cls):
        cls.recall_id = recall_functions.recall_create()
        cls.args['recall_id'] = cls.recall_id

    @classmethod
    def tearDownClass(cls):
        if cls.recall_id is not None:
            recall_functions.recall_delete(cls.recall_id)

    def test_remedy_create_success(self):
        remedy_id = recall_functions.remedy_create(self.args)
        recall = recall_functions.recall_get(self.recall_id)
        self.assertTrue(recall.get('remedy_id', None) == remedy_id)
        if remedy_id is not None:
            recall_functions.remedy_delete({'remedy_id': remedy_id})

    # test errors
    def test_remedy_create_error_input_null_recall_id(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = None
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_create(args)

    def test_remedy_create_error_null_description(self):
        args = copy.deepcopy(self.args)
        args['description'] = None
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_create(args)

    def test_remedy_create_error_add_remedy_to_recall_that_already_has_remedy(self):
        recall_id2 = recall_functions.recall_create()
        args = copy.deepcopy(self.args)
        args['recall_id'] = recall_id2
        recall_functions.remedy_create(args)
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_create(args)

    def test_remedy_create_error_input_invalid_recall_id(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = self.recall_id_invalid
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_create(args)

    def test_remedy_create_error_input_invalid_type_recall_id(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_create(args)

    def test_remedy_create_error_input_invalid_type_description(self):
        args = copy.deepcopy(self.args)
        args['description'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_create(args)

    def test_remedy_create_error_input_invalid_recall_id_must_be_positive_integer(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = -1
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_create(args)

    def test_remedy_create_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            recall_functions.remedy_create(self.args, False)


@arcimoto.runtime.handler
def test_remedy_create():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RecallRemedyCreateTestCase)
    ))


lambda_handler = test_remedy_create
