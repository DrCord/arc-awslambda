import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'recall_id': {
        'type': 'integer',
        'required': True,
        'min': 1
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('recalls.recall.delete')
@arcimoto.db.transaction
def recall_delete(recall_id):
    global logger

    cursor = arcimoto.db.get_cursor()

    query = (
        'UPDATE recalls '
        'SET status = \'deleted\' '
        'WHERE id = %s '
        'returning id'
    )
    record_to_delete = [recall_id]
    cursor.execute(query, record_to_delete)

    result_set = cursor.fetchone()
    recall_id = result_set['id'] if result_set is not None else None

    return {'recall_id': recall_id}


lambda_handler = recall_delete
