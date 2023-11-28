import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'first': {
        'type': 'boolean',
        'nullable': True
    },
    'last': {
        'type': 'boolean',
        'nullable': True
    },
    'id': {
        'type': 'integer',
        'min': 0,
        'nullable': True
    }
})


@arcimoto.runtime.handler
def recall_get_updated(first=False, last=False, id=None):
    global logger

    if first and last:
        raise ArcimotoArgumentError('first and last are mutually exclusive options, only 1 can be set to true')

    if not first and not last and id is None:
        raise ArcimotoArgumentError('id is a required argument if the first and last booleans are both false')

    cursor = arcimoto.db.get_cursor()

    query = (
        'SELECT value '
        'FROM meta '
        'where section = \'recall_data_update\' '
    )
    if first:
        query += (
            'ORDER BY value '
            'ASC LIMIT 1'
        )
    elif last:
        query += (
            'ORDER BY value '
            'DESC LIMIT 1'
        )
    else:
        query += (
            'AND key = \'%s\''
        )
    if first or last:
        cursor.execute(query)
    else:
        cursor.execute(query, [id])

    recall_data_update = cursor.fetchone()

    return {
        'value': recall_data_update.get('value', None)
    }


lambda_handler = recall_get_updated
