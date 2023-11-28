import logging
import unittest
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import notes_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class NotesGetTestCase(unittest.TestCase):

    args = {
        'object_type': 'Vehicle',
        'object_id': arcimoto.tests.uuid_vin_get(),
        'note_id': None,
        'tags': None,
        'created': None,
        'author': None
    }

    @classmethod
    def setUpClass(cls):
        cls.notes_original_length = len(notes_functions.notes_get())
        cls.note_id = notes_functions.note_create()

    def test_notes_get_success(self):
        notes_length = len(notes_functions.notes_get())
        self.assertTrue(notes_length == self.notes_original_length + 1)
        if self.note_id is not None:
            notes_functions.note_delete(self.note_id)
        notes_length = len(notes_functions.notes_get())
        self.assertTrue(notes_length == self.notes_original_length)

    # test errors
    def test_notes_get_error_input_null_object_type(self):
        args = copy.deepcopy(self.args)
        args['object_type'] = None
        with self.assertRaises(ArcimotoArgumentError):
            notes_functions.notes_get(args)

    def test_notes_get_error_input_null_object_id(self):
        args = copy.deepcopy(self.args)
        args['object_id'] = None
        with self.assertRaises(ArcimotoArgumentError):
            notes_functions.notes_get(args)

    def test_notes_get_error_input_invalid_note_id_must_be_positive_integer(self):
        args = copy.deepcopy(self.args)
        args['note_id'] = -1
        with self.assertRaises(ArcimotoArgumentError):
            notes_functions.notes_get(args)

    def test_notes_get_error_input_invalid_type_object_type(self):
        args = copy.deepcopy(self.args)
        args['object_type'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            notes_functions.notes_get(args)

    def test_notes_get_error_input_invalid_type_note_id(self):
        args = copy.deepcopy(self.args)
        args['note_id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            notes_functions.notes_get(args)

    def test_notes_get_error_input_invalid_type_tags(self):
        args = copy.deepcopy(self.args)
        args['tags'] = 'not a list'
        with self.assertRaises(ArcimotoArgumentError):
            notes_functions.notes_get(args)

    def test_notes_get_error_input_invalid_type_created(self):
        args = copy.deepcopy(self.args)
        args['created'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            notes_functions.notes_get(args)

    def test_notes_get_error_input_invalid_type_created(self):
        args = copy.deepcopy(self.args)
        args['author'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            notes_functions.notes_get(args)


@arcimoto.runtime.handler
def test_notes_get():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(NotesGetTestCase)
    ))


lambda_handler = test_notes_get
