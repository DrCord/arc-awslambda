import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db
import arcimoto.args

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'recall_id': {
        'type': 'integer',
        'required': True,
        'min': 1
    },
    'title': {
        'type': 'string',
        'nullable': True,
        'default': None,
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    },
    'description': {
        'type': 'string',
        'nullable': True,
        'default': None,
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    },
    'nhtsa_number': {
        'type': 'string',
        'nullable': True,
        'default': None,
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    },
    'date': {
        'type': 'string',
        'nullable': True,
        'default': None,
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    },
    'mfr_campaign_id': {
        'type': 'string',
        'nullable': True,
        'default': None,
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    },
    'country': {
        'type': 'string',
        'nullable': True,
        'default': None,
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    },
    'safety_recall': {
        'type': 'boolean',
        'nullable': True,
        'default': None,
        'coerce': (str, arcimoto.args.arg_boolean_empty_string_to_null)
    },
    'safety_description': {
        'type': 'string',
        'nullable': True,
        'default': None,
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    },
    'remedy_id': {
        'type': 'integer',
        'nullable': True,
        'min': 1,
        'default': None,
        'coerce': (str, arcimoto.args.arg_integer_empty_string_to_null)
    },
    'status': {
        'type': 'string',
        'nullable': True,
        'allowed': ['active', 'deleted'],
        'default': None,
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('recalls.recall.edit')
@arcimoto.db.transaction
def recall_edit(recall_id, title=None, description=None, nhtsa_number=None, date=None, mfr_campaign_id=None, country=None, safety_recall=None, safety_description=None, remedy_id=None, status=None):
    global logger
    cursor = arcimoto.db.get_cursor()

    if safety_recall:
        if not safety_description:
            raise ArcimotoArgumentError('if safety_recall is true then safety_description is a required argument')
    else:
        # ignore safety_description input if safety_recall boolean is not true
        safety_description = None

    if not title and not description and not nhtsa_number and not date and not mfr_campaign_id and not country and safety_recall is None and not safety_description and not remedy_id and not status:
        raise ArcimotoArgumentError('You must supply title, description, nhtsa_number, date, mfr_campaign_id, country, safety_recall, safety_description, remedy_id or status to edit the record')

    where_predicates = [
        {
            'column': 'id',
            'operator': '=',
            'value': recall_id
        }
    ]
    columns_data = [
        {'mfr_campaign_id': mfr_campaign_id},
        {'country': country},
        {'title': title},
        {'description': description},
        {'nhtsa_number': nhtsa_number},
        {'date': date},
        {'remedy_id': remedy_id},
        {'safety_recall': safety_recall},
        {'safety_description': safety_description if safety_recall is True else None},
        {'status': status}
    ]
    cursor.execute(*arcimoto.db.prepare_update_query_and_params('recalls', where_predicates, columns_data))
    recall = cursor.fetchone()

    return {
        'recall_id': recall['id'],
        'mfr_campaign_id': recall['mfr_campaign_id'],
        'country': recall['country'],
        'title': recall['title'],
        'description': recall['description'],
        'nhtsa_number': recall['nhtsa_number'],
        'date': arcimoto.db.datetime_record_output(recall['date']),
        'remedy_id': recall['remedy_id'],
        'safety_recall': recall['safety_recall'],
        'safety_description': recall['safety_description'],
        'status': recall['status']
    }


lambda_handler = recall_edit
