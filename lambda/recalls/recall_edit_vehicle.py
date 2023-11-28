import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

import recalls as recalls_class

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'id': {
        'type': 'integer',
        'required': False,
        'nullable': True,
        'min': 1,
        'coerce': (str, arcimoto.args.arg_integer_empty_string_to_null)
    },
    'recall_id': {
        'type': 'integer',
        'required': False,
        'nullable': True,
        'min': 1,
        'dependencies': 'vin',
        'coerce': (str, arcimoto.args.arg_integer_empty_string_to_null)
    },
    'service_date': {
        'type': 'string',
        'required': False,
        'nullable': True,
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    },
    'service_reference': {
        'type': 'string',
        'required': False,
        'nullable': True,
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    },
    'vin': {
        'type': 'string',
        'required': False,
        'nullable': True,
        'dependencies': 'recall_id',
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('recalls.vehicle.edit')
@arcimoto.db.transaction
def recall_edit_vehicle(id, recall_id, service_date, service_reference, vin):
    global logger

    cursor = arcimoto.db.get_cursor()
    prequery_validation(cursor, id, recall_id, service_date, service_reference, vin)

    # query
    columns_data = [
        {'service_date': service_date},
        {'service_reference': service_reference}
    ]

    if id is not None:
        where_predicates = [
            {
                'column': 'id',
                'operator': '=',
                'value': id
            }
        ]
        columns_data.append({'recall_id': recall_id})
        columns_data.append({'vin': vin})
    else:
        where_predicates = [
            {
                'column': 'recall_id',
                'operator': '=',
                'value': recall_id
            },
            {
                'column': 'vin',
                'operator': '=',
                'value': vin
            }
        ]
    cursor.execute(*arcimoto.db.prepare_update_query_and_params('vehicle_recalls', where_predicates, columns_data))

    result = cursor.fetchone()

    return {
        'id': result['id'],
        'recall_id': result['recall_id'],
        'service_date': arcimoto.db.datetime_record_output(result['service_date']),
        'service_reference': result['service_reference'],
        'vin': result['vin']
    }


def prequery_validation(cursor, id, recall_id, service_date, service_reference, vin):
    recalls_resources = recalls_class.Recalls()

    if not recall_id and not service_date and not service_reference and not vin:
        raise ArcimotoArgumentError('Either recall_id or service_date or service reference or vin are required to make an edit')

    if id is not None:
        if recalls_resources.vehicle_recall_exists(id) is False:
            raise ArcimotoArgumentError('vehicle recall id {} does not exist'.format(id))
    else:
        if recalls_resources.recall_exists(recall_id) is False:
            raise ArcimotoArgumentError('recall_id {} does not exist'.format(recall_id))

        if recalls_resources.vehicle_exists(vin) is False:
            raise ArcimotoArgumentError('vin {} does not exist'.format(vin))

    # check if edit is changing VIN and that VIN already exists in this recall, if so reject with error
    if id is not None and vin is not None:
        query = (
            'SELECT recall_id '
            'FROM vehicle_recalls '
            'WHERE id=%s'
        )
        cursor.execute(query, [id])
        recall_id_selected = cursor.fetchone()
        query = (
            'SELECT vin '
            'FROM vehicle_recalls '
            'WHERE vin=%s '
            'AND recall_id = %s '
            'AND id != %s'
        )
        cursor.execute(query, [vin, recall_id_selected[0], id])
        vehicle_recall = cursor.fetchone()
        if vehicle_recall is not None:
            raise ArcimotoArgumentError('vin {} already exists for recall {}'.format(vin, recall_id_selected[0]))


lambda_handler = recall_edit_vehicle
