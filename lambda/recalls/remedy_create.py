import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

import recalls as recalls_class

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'recall_id': {
        'type': 'integer',
        'required': True,
        'min': 1
    },
    'description': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('recalls.recall.create')
@arcimoto.user.require('recalls.recall.edit')
@arcimoto.db.transaction
def remedy_create(recall_id, description):
    global logger

    cursor = arcimoto.db.get_cursor()
    recalls_resources = recalls_class.Recalls()

    if recalls_resources.recall_exists(recall_id) is False:
        raise ArcimotoArgumentError('recall id {} does not exist'.format(recall_id))

    if recalls_resources.recall_has_remedy(recall_id) is True:
        raise ArcimotoArgumentError('remedy already exists for recall id {}'.format(recall_id))

    query = (
        'INSERT into recall_remedies '
        '(description) '
        'values (%s) '
        'ON CONFLICT DO NOTHING '
        'RETURNING id'
    )
    cursor.execute(query, [description])

    result_set = cursor.fetchone()
    remedy_id = result_set['id'] if result_set is not None else None
    if remedy_id is None:
        raise ArcimotoException('Remedy id not returned from insert query, without the remedy id we cannot link the remedy to the recall')

    query = (
        'UPDATE recalls '
        'SET remedy_id = %s '
        'WHERE id = %s'
    )
    cursor.execute(query, [remedy_id, recall_id])

    return {
        'remedy_id': remedy_id
    }


lambda_handler = remedy_create
