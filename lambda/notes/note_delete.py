import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'note_id': {
        'type': 'integer',
        'required': True,
        'min': 1
    },
})


@arcimoto.runtime.handler
@arcimoto.user.require('notes.note.delete')
@arcimoto.db.transaction
def note_delete(note_id):
    '''delete note and tag joins from database'''

    cursor = arcimoto.db.get_cursor()

    query = (
        'DELETE FROM '
        'notes '
        'WHERE '
        'note_id = %s'
    )
    cursor.execute(query, [note_id])
    query = (
        'DELETE FROM '
        'notes_tags_join '
        'WHERE '
        'note_id = %s'
    )
    cursor.execute(query, [note_id])

    return {}


lambda_handler = note_delete
