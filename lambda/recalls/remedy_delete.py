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
@arcimoto.user.require('recalls.recall.edit')
@arcimoto.user.require('recalls.recall.delete')
@arcimoto.db.transaction
def remedy_delete(remedy_id):
    global logger

    cursor = arcimoto.db.get_cursor()
    query = (
        'DELETE from recall_remedies '
        'WHERE id = %s '
        'RETURNING id'
    )
    cursor.execute(query, [remedy_id])
    result_set = cursor.fetchone()
    remedy_id = result_set['id'] if result_set is not None else None
    if remedy_id is None:
        raise ArcimotoException('remedy_id not returned from remedy delete query, cannot remove link between remedy and recall')
    # remove remedy record link from recalls table
    query = (
        'UPDATE recalls '
        'SET remedy_id = NULL '
        'WHERE remedy_id = %s'
    )
    cursor.execute(query, [remedy_id])

    return {'remedy_id': remedy_id}


lambda_handler = remedy_delete
