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
    'vehicle_recall_id': {
        'type': 'integer',
        'min': 1
    },
    'recall_id': {
        'type': 'integer',
        'min': 1,
        'dependencies': 'vins'
    },
    'vins': {
        'type': 'list',
        'dependencies': 'recall_id',
        'empty': False
    },
    'service_reference': {
        'type': 'string',
        'required': False,
        'nullable': True,
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    },
    'service_date': {
        'type': 'string',
        'required': False,
        'nullable': True,
        'coerce': (str, arcimoto.args.arg_string_empty_string_to_null)
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('recalls.vehicle.service')
@arcimoto.db.transaction
def recall_service_vehicle(vehicle_recall_id=None, recall_id=None, vins=None, service_reference=None, service_date=None):
    global logger

    vehicle_service_records = []

    cursor = arcimoto.db.get_cursor()
    prequery_validation(vehicle_recall_id, recall_id, vins)

    params = []
    query = (
        'UPDATE vehicle_recalls '
    )
    query_end = (
        'RETURNING '
        'id, '
        'recall_id, '
        'service_date, '
        'service_reference, '
        'vin'
    )
    if service_date is not None:
        query += 'SET service_date = %s '
        params.append(service_date)
    else:
        query += 'SET service_date = NOW() '

    if service_reference is not None:
        query += ', service_reference = %s '
        params.append(service_reference)
    if vehicle_recall_id is not None:
        query += 'WHERE id = %s '
        params.append(vehicle_recall_id)
        query += query_end
        cursor.execute(query, params)
        vehicle_recall = cursor.fetchone()
        vehicle_service_records.append({
            'vehicles_serviced': vehicle_recall['id'],
            'recall_id': vehicle_recall['recall_id'],
            'service_date': arcimoto.db.datetime_record_output(vehicle_recall['service_date']),
            'service_reference': vehicle_recall['service_reference'],
            'vin': vehicle_recall['vin']
        })
    else:
        query += (
            'WHERE recall_id = %s '
            'AND vin = %s '
        )
        params.append(recall_id)

        query += query_end
        for vin in vins:
            params_with_vin = params + [vin]
            cursor.execute(query, params_with_vin)
            vehicle_recall = cursor.fetchone()
            vehicle_service_records.append({
                'id': vehicle_recall['id'],
                'recall_id': vehicle_recall['recall_id'],
                'service_date': arcimoto.db.datetime_record_output(vehicle_recall['service_date']),
                'service_reference': vehicle_recall['service_reference'],
                'vin': vehicle_recall['vin']
            })

    return {
        'vehicle_service_records': vehicle_service_records
    }


def prequery_validation(vehicle_recall_id, recall_id, vins):
    recalls_resources = recalls_class.Recalls()

    if not vehicle_recall_id and (not recall_id or not vins):
        raise ArcimotoArgumentError('recall_id and vins are required together if you do not use the vehicle_recall_id parameter')

    if vehicle_recall_id is not None:
        if recalls_resources.vehicle_recall_exists(vehicle_recall_id) is False:
            raise ArcimotoArgumentError('id {} does not exist in vehicle_recalls table'.format(vehicle_recall_id))
    else:
        if recalls_resources.recall_exists(recall_id) is False:
            raise ArcimotoArgumentError('recall_id {} does not exist in vehicle_recalls table'.format(recall_id))

        errors = []
        for vin in vins:
            if recalls_resources.vehicle_exists(vin) is False:
                errors.append('vin {} does not exist'.format(vin))
        if len(errors):
            if len(errors) == 1:
                raise ArcimotoArgumentError(errors[0])
            else:
                msg = "\n" + "\n".join(errors)
                raise ArcimotoArgumentError(f'Errors:{msg}')


lambda_handler = recall_service_vehicle
