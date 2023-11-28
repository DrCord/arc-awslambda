import logging
import unittest
import copy
from datetime import datetime

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import recall_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RecallRemedyEditTestCase(unittest.TestCase):

    args = {
        'remedy_id': None,
        'description': 'Edited by unit tests',
        'date': str(datetime.now())
    }

    @classmethod
    def setUpClass(cls):
        cls.recall_id = recall_functions.recall_create()
        args = {
            'recall_id': cls.recall_id,
            'description': 'Created by unit test script'
        }
        cls.remedy_id = recall_functions.remedy_create(args)
        cls.args['remedy_id'] = cls.remedy_id

    @classmethod
    def tearDownClass(cls):
        if cls.remedy_id is not None:
            recall_functions.remedy_delete({'remedy_id': cls.remedy_id})
        if cls.recall_id is not None:
            recall_functions.recall_delete(cls.recall_id)

    def test_remedy_edit_success_input_date_and_description(self):
        args = copy.deepcopy(self.args)
        self.assertIsInstance(recall_functions.remedy_edit(args), dict)

    def test_remedy_edit_success_input_date(self):
        args = copy.deepcopy(self.args)
        args['description'] = None
        self.assertIsInstance(recall_functions.remedy_edit(args), dict)

    def test_remedy_edit_success_input_description(self):
        args = copy.deepcopy(self.args)
        args['date'] = None
        self.assertIsInstance(recall_functions.remedy_edit(args), dict)

    # test errors
    def test_remedy_edit_error_input_null_remedy_id(self):
        args = copy.deepcopy(self.args)
        args['remedy_id'] = None
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_edit(args)

    def test_remedy_edit_error_input_no_edits(self):
        args = copy.deepcopy(self.args)
        args['date'] = None
        args['description'] = None
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_edit(args)

    def test_remedy_edit_error_input_remedy_id_must_be_positive_integer(self):
        args = copy.deepcopy(self.args)
        args['remedy_id'] = -1
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_edit(args)

    def test_remedy_edit_error_input_invalid_type_remedy_id(self):
        args = copy.deepcopy(self.args)
        args['remedy_id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_edit(args)

    def test_remedy_edit_error_input_invalid_type_date(self):
        args = copy.deepcopy(self.args)
        args['date'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_edit(args)

    def test_remedy_edit_error_input_invalid_type_description(self):
        args = copy.deepcopy(self.args)
        args['description'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.remedy_edit(args)

    def test_remedy_edit_error_user_unauthorized(self):
        args = copy.deepcopy(self.args)
        with self.assertRaises(ArcimotoPermissionError):
            recall_functions.remedy_edit(args, False)


@arcimoto.runtime.handler
def test_remedy_edit():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RecallRemedyEditTestCase)
    ))


lambda_handler = test_remedy_edit
