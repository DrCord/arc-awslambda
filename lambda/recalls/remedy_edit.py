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
    },
    'date': {
        'type': 'string',
        'nullable': True,
        'required': False
    },
    'description': {
        'type': 'string',
        'nullable': True,
        'required': False
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('recalls.recall.edit')
@arcimoto.db.transaction
def remedy_edit(remedy_id, date=None, description=None):
    global logger

    cursor = arcimoto.db.get_cursor()

    if not date and not description:
        raise ArcimotoArgumentError('You must supply either date or description to edit the record')

    # query
    columns_data = []
    if date:
        columns_data.append({'date': date})
    if description:
        columns_data.append({'description': description})

    where_predicates = [
        {
            'column': 'id',
            'operator': '=',
            'value': remedy_id
        }
    ]
    cursor.execute(*arcimoto.db.prepare_update_query_and_params('recall_remedies', where_predicates, columns_data))
    result = cursor.fetchone()

    return {
        'remedy_id': result['id'],
        'date': arcimoto.db.datetime_record_output(result['date']),
        'description': result['description']
    }


lambda_handler = remedy_edit
