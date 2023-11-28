import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'updated': {
        'type': 'string',
        'required': False,
        'nullable': True,
        'default': None
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('recalls.updated.write')
@arcimoto.db.transaction
def recall_set_updated(updated):
    global logger

    cursor = arcimoto.db.get_cursor()
    # get all keys (0 indexed) and use len to be the next key for the inserted data
    query = (
        'SELECT key '
        'FROM meta '
        'WHERE section = \'recall_data_update\''
    )
    cursor.execute(query)
    recall_data_updates_len = len(cursor.fetchall())

    query = 'INSERT INTO meta (section, key, value) '

    if updated is None:
        query += (
            'VALUES (\'recall_data_update\', %s, NOW()) '
            'ON CONFLICT (section, key) DO UPDATE SET value = NOW() '
        )
    else:
        query += (
            'VALUES (\'recall_data_update\', %s, %s) '
            'ON CONFLICT (section, key) DO UPDATE SET value = %s '
        )

    query += 'RETURNING section, key, value'

    if updated is None:
        cursor.execute(query, [recall_data_updates_len])
    else:
        cursor.execute(query, [recall_data_updates_len, updated, updated])

    recall_meta_record = cursor.fetchone()

    return {
        'section': recall_meta_record['section'],
        'key': recall_meta_record['key'],
        'value': recall_meta_record['value'],
    }


lambda_handler = recall_set_updated
