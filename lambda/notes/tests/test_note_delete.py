import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import notes_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class NoteDeleteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_vin = arcimoto.tests.test_vin_get()
        cls.notes_original_length = len(notes_functions.notes_get())
        cls.note_id = notes_functions.note_create()
        cls.notes_length = len(notes_functions.notes_get())

    def test_note_delete_success(self):
        self.assertTrue(self.notes_length == self.notes_original_length + 1)
        notes_functions.note_delete(self.note_id)
        self.notes_length = len(notes_functions.notes_get())
        self.assertTrue(self.notes_length == self.notes_original_length)

    # test errors
    def test_note_delete_error_null_note_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            notes_functions.note_delete(None)

    def test_note_delete_error_input_invalid_type_note_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            notes_functions.note_delete('not an integer')

    def test_note_delete_error_user_unauthorized(self):
        note_id = notes_functions.note_create()
        with self.assertRaises(ArcimotoPermissionError):
            notes_functions.note_delete(note_id, False)
        notes_functions.note_delete(note_id)


@arcimoto.runtime.handler
def test_note_delete():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(NoteDeleteTestCase)
    ))


lambda_handler = test_note_delete
