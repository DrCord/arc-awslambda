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
    'note_id': {
        'type': 'integer',
        'min': 1,
        'nullable': True
    },
    'tags': {
        'type': 'list',
        'nullable': True
    },
    'created': {
        'type': 'string',
        'nullable': True
    },
    'author': {
        'type': 'string',
        'nullable': True
    }
})


@arcimoto.runtime.handler
# no specific permission required to get notes
def notes_get(object_type, object_id, note_id=None, tags=None, created=None, author=None):
    '''Query database and retreive notes'''
    notes = []
    cursor = arcimoto.db.get_cursor()

    query_params = {
        'object_type': object_type,
        'object_id': object_id,
        'note_id': note_id,
        'created': created,
        'author': author,
    }
    query, values = build_query(query_params)
    cursor.execute(query, values)
    results = cursor.fetchall()

    for item in results:
        note = {
            'note_id': item['note_id'],
            'created': str(item['created']),
            'author': item['author'],
            'content': item['content'],
        }
        # get tags
        query = (
            'SELECT tag_name '
            'FROM notes_tags '
            'INNER JOIN notes_tags_join '
            'ON notes_tags.tag_id = notes_tags_join.tag_id '
            'WHERE notes_tags_join.note_id =%s'
        )
        cursor.execute(query, [note['note_id']])
        tags_query_result = cursor.fetchall()
        note['tags'] = [tag[0] for tag in tags_query_result]

        # filter by tags
        if tags:
            if [t for t in note['tags'] if any(i in t for i in tags)]:
                notes.append(note)
        else:
            notes.append(note)
    return notes


def build_query(params):
    '''Generate sql query from params'''
    keys = []
    values = []
    query = (
        'SELECT note_id, created, author, content '
        'FROM notes '
        'WHERE '
    )
    for p in params.keys():
        if params[p] is not None:
            keys.append('{}=%s'.format(p))
            values.append(params[p])
    query += '{}'.format(' AND '.join(keys))
    return query, values


lambda_handler = notes_get
