import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'remedy_id': {
        'type': 'integer',
        'required': True,
        'min': 1
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('recalls.recall.read')
def remedy_get(remedy_id):
    global logger

    cursor = arcimoto.db.get_cursor()

    query = (
        'SELECT id, date, description '
        'FROM recall_remedies '
        'WHERE id=%s'
    )
    cursor.execute(query, [remedy_id])
    if cursor.rowcount != 1:
        raise Exception('Invalid remedy id')
    remedy = cursor.fetchone()

    return {
        'remedy_id': remedy['id'],
        'date': arcimoto.db.datetime_record_output(remedy['date']),
        'description': remedy['description']
    }


lambda_handler = remedy_get
