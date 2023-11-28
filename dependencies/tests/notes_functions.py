import logging
import boto3

import arcimoto.runtime
import arcimoto.tests

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

test_vin = arcimoto.tests.test_vin_get()


def note_create(args=None, test_runner_user_admin=True):
    global test_vin
    if args is None:
        args = {
            'object_type': 'Vehicle',
            'object_id': test_vin,
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
    note = arcimoto.runtime.test_invoke_lambda('note_create', args, test_runner_user_admin)
    return note.get('note_id', None)


def note_delete(note_id, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('note_delete', {'note_id': note_id}, test_runner_user_admin)


def notes_get(args=None, test_runner_user_admin=True):
    global test_vin
    if args is None:
        args = {
            "note_id": None,
            "tags": None,
            "object_type": 'Vehicle',
            "object_id": test_vin,
            "created": None,
            "author": None,
        }
    return arcimoto.runtime.test_invoke_lambda('notes_get', args, test_runner_user_admin)
