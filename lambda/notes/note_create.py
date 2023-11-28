import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'object_type': {
        'type': 'string',
        'required': True
    },
    'object_id': {
        'required': True
    },
    'content': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'author': {
        'type': 'string',
        'nullable': True
    },
    'tags': {
        'type': 'list',
        'nullable': True
    }
})


@arcimoto.runtime.handler
@arcimoto.db.transaction
def note_create(object_type, object_id, content, author=None, tags=None):
    """create note and add to database"""
    global logger

    cursor = arcimoto.db.get_cursor()

    query = (
        'INSERT INTO notes '
        '(object_type, object_id, author, content) '
        'VALUES (%s, %s, %s, %s) '
        'RETURNING notes.note_id'
    )
    if author is None:
        author = arcimoto.user.current().get_username()
    if author is None:
        author = 'Arcimoto'
    cursor.execute(query, [object_type, str(object_id), author, content])
    note_id = cursor.fetchone()[0]

    for tag in tags:
        # create / get tag_id
        query = (
            'SELECT tag_id '
            'FROM notes_tags '
            'WHERE tag_name=%s'
        )
        cursor.execute(query, [tag])
        data = cursor.fetchone()
        if data:
            tag_id = data[0]
        else:
            query = (
                'INSERT INTO notes_tags '
                '(tag_name) VALUES (%s) '
                'RETURNING tag_id'
            )
            cursor.execute(query, [tag])
            tag_id = cursor.fetchone()[0]

        # create entry in join table
        query = (
            'INSERT INTO notes_tags_join '
            '(note_id, tag_id) VALUES (%s, %s)'
        )
        cursor.execute(query, [note_id, tag_id])

    return {"note_id": note_id}


lambda_handler = note_create
