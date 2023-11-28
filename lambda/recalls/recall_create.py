import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db
import arcimoto.args

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


arcimoto.args.register({
    'title': {
        'type': 'string',
        'required': True,
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    },
    'description': {
        'type': 'string',
        'required': True,
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    },
    'nhtsa_number': {
        'type': 'string',
        'required': True,
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    },
    'mfr_campaign_id': {
        'type': 'string',
        'nullable': True,
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    },
    'country': {
        'type': 'string',
        'nullable': True,
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    },
    'safety_recall': {
        'type': 'boolean',
        'required': True,
        'coerce': (str, arcimoto.args.arg_boolean_empty_string_to_null)
    },
    'safety_description': {
        'type': 'string',
        'nullable': True,
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('recalls.recall.create')
@arcimoto.db.transaction
def recall_create(title, description, nhtsa_number, mfr_campaign_id, country, safety_recall, safety_description):
    global logger

    cursor = arcimoto.db.get_cursor()

    if safety_recall:
        if not safety_description:
            raise ArcimotoArgumentError('if safety_recall is true then safety_description is a required argument')
    else:
        # ignore safety_description input if safety_recall boolean is not true
        safety_description = None

    # create setup default data to make query building simpler
    columns = ['title', 'description', 'nhtsa_number']
    # required fields
    column_values = [title, description, nhtsa_number]
    value_placeholders = ['%s', '%s', '%s']
    # non-required fields
    if mfr_campaign_id is not None:
        columns.append('mfr_campaign_id')
        column_values.append(mfr_campaign_id)
        value_placeholders.append('%s')
    if country is not None:
        columns.append('country')
        column_values.append(country)
        value_placeholders.append('%s')
    if safety_recall:
        columns.append('safety_recall')
        column_values.append(safety_recall)
        value_placeholders.append('%s')
        columns.append('safety_description')
        column_values.append(safety_description)
        value_placeholders.append('%s')

    query = (
        'INSERT INTO recalls '
        '({}) '
        'VALUES ({}) '
        'ON CONFLICT DO NOTHING '
        'RETURNING recalls.*'
    )
    insert_query = query.format(', '.join(columns), ' ,'.join(value_placeholders))
    cursor.execute(insert_query, column_values)

    result_set = cursor.fetchone()
    recall_id = result_set['id'] if result_set is not None else None

    return {
        'id': result_set['id'],
        'title': result_set['title'],
        'description': result_set['description'],
        'nhtsa_number': result_set['nhtsa_number'],
        'date': arcimoto.db.datetime_record_output(result_set['date']),
        'mfr_campaign_id': result_set['mfr_campaign_id'],
        'country': result_set['country'],
        'safety_recall': result_set['safety_recall'],
        'safety_description': result_set['safety_description'],
        'remedy_id': result_set['remedy_id'],
        'status': result_set['status']
    }


lambda_handler = recall_create
