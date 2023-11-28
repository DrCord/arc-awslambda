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


class NoteCreateTestCase(unittest.TestCase):

    args = {
        'object_type': 'Vehicle',
        'object_id': arcimoto.tests.uuid_vin_get(),
        'author': 'UNIT_TEST',
        'content': 'created by unit test',
        'tags': [
            'service',
            'firmware',
            'delivery',
            'manufacturing',
            'quality',
            'debugging'
        ]
    }

    @classmethod
    def setUpClass(cls):
        arcimoto.tests.vehicle_create(cls.args['object_id'])

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.args['object_id'])

    def test_note_create_success(self):
        note_id = notes_functions.note_create()
        self.assertTrue(note_id is not None)
        notes_functions.note_delete(note_id)

    # test errors
    def test_note_create_error_input_null_object_type(self):
        args = copy.deepcopy(self.args)
        args['object_type'] = None
        with self.assertRaises(ArcimotoArgumentError):
            notes_functions.note_create(args)

    def test_note_create_error_input_null_object_id(self):
        args = copy.deepcopy(self.args)
        args['object_id'] = None
        with self.assertRaises(ArcimotoArgumentError):
            notes_functions.note_create(args)

    def test_note_create_error_input_null_content(self):
        args = copy.deepcopy(self.args)
        args['content'] = None
        with self.assertRaises(ArcimotoArgumentError):
            notes_functions.note_create(args)

    def test_note_create_error_input_invalid_type_object_type(self):
        args = copy.deepcopy(self.args)
        args['object_type'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            notes_functions.note_create(args)

    def test_note_create_error_input_invalid_type_content(self):
        args = copy.deepcopy(self.args)
        args['content'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            notes_functions.note_create(args)


@arcimoto.runtime.handler
def test_note_create():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(NoteCreateTestCase)
    ))


lambda_handler = test_note_create
