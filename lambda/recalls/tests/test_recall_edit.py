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


class RecallEditTestCase(unittest.TestCase):

    args = {
        'recall_id': None,
        'title': 'TEST-EDITED-RECALL',
        'description': 'Edited by unit tests',
        'nhtsa_number': None,
        'date': None,
        'mfr_campaign_id': None,
        'country': None,
        'safety_recall': None,
        'safety_description': None
    }

    @property
    def recall_id_invalid(self):
        return (self.recall_id if self.recall_id is not None else recall_functions.recall_create()) + 1

    @classmethod
    def setUpClass(cls):
        cls.recall_id = recall_functions.recall_create()
        cls.args['recall_id'] = cls.recall_id

    @classmethod
    def tearDownClass(cls):
        if cls.recall_id is not None:
            recall_functions.recall_delete(cls.recall_id)

    def test_recall_edit_success_single_edit(self):
        args = copy.deepcopy(self.args)
        args['description'] = None
        recall = recall_functions.recall_edit(args)
        self.assertTrue(recall.get('title', None) == self.args['title'])

    def test_recall_edit_success_multiple_edits(self):
        args = copy.deepcopy(self.args)
        recall = recall_functions.recall_edit(args)
        self.assertTrue(recall.get('title', None) == self.args['title'])
        self.assertTrue(recall.get('description', None) == self.args['description'])

    # test errors
    def test_recall_edit_error_input_invalid_recall_id(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = None
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit(args)

    def test_recall_edit_error_input_invalid_status(self):
        args = copy.deepcopy(self.args)
        args['status'] = 'invalid value'
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit(args)

    def test_recall_edit_error_no_edits(self):
        args = copy.deepcopy(self.args)
        args['title'] = None
        args['description'] = None
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit(args)

    def test_recall_edit_error_input_invalid_type_recall_id(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit(args)

    def test_recall_edit_error_input_invalid_type_safety_recall(self):
        args = copy.deepcopy(self.args)
        args['safety_recall'] = 'not a boolean'
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit(args)

    def test_recall_edit_error_input_invalid_type_remedy_id(self):
        args = copy.deepcopy(self.args)
        args['remedy_id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit(args)

    def test_recall_edit_error_input_invalid_recall_id_must_be_positive_integer(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = -1
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit(args)

    def test_recall_edit_error_input_invalid_remedy_id_must_be_positive_integer(self):
        args = copy.deepcopy(self.args)
        args['remedy_id'] = -1
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit(args)

    def test_recall_edit_error_user_unauthorized(self):
        args = copy.deepcopy(self.args)
        with self.assertRaises(ArcimotoPermissionError):
            recall_functions.recall_edit(args, False)


@arcimoto.runtime.handler
def test_recall_edit():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RecallEditTestCase)
    ))


lambda_handler = test_recall_edit
