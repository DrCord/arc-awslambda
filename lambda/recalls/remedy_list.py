import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({})


@arcimoto.runtime.handler
@arcimoto.user.require('recalls.recall.read')
def remedy_list():
    global logger

    cursor = arcimoto.db.get_cursor()

    query = (
        'SELECT '
        'id, '
        'date, '
        'description '
        'FROM recall_remedies '
        'ORDER BY id ASC'
    )
    cursor.execute(query)
    remedies = []
    for record in cursor:
        remedies.append(
            {
                'remedy_id': record['id'],
                'date': arcimoto.db.datetime_record_output(record['date']),
                'description': record['description']
            }
        )

    return {'remedies': remedies}


lambda_handler = remedy_list
