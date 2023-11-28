import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'id': {
        'type': 'integer',
        'nullable': True,
        'min': 1,
        'default': None
    },
    'recall_id': {
        'type': 'integer',
        'nullable': True,
        'min': 1,
        'dependencies': 'vin',
        'default': None
    },
    'vin': {
        'type': 'string',
        'nullable': True,
        'dependencies': 'recall_id',
        'default': None
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('recalls.vehicle.read')
def recall_get_vehicle(id=None, recall_id=None, vin=None):
    global logger

    cursor = arcimoto.db.get_cursor()

    if not id and (not recall_id or not vin):
        raise ArcimotoArgumentError('recall_id and vin are required together')

    if not recall_id and not vin and not id:
        raise ArcimotoArgumentError('Either id or recall_id and vin are required')

    query = (
        'SELECT id, recall_id, service_date, service_reference, vin '
        'FROM vehicle_recalls '
    )
    if id is not None:
        query += (
            'WHERE id = %s'
        )
        params = [id]
    else:
        query += (
            'WHERE recall_id = %s '
            'AND vin = %s'
        )
        params = [recall_id, vin]
    cursor.execute(query, params)

    if cursor.rowcount != 1:
        raise ArcimotoNotFoundError('Invalid vehicle_recalls input parameters')

    recall = cursor.fetchone()

    return {
        'vehicle_recall_id': recall['id'],
        'recall_id': recall['recall_id'],
        'service_date': arcimoto.db.datetime_record_output(recall['service_date']),
        'service_reference': recall['service_reference'],
        'vin': recall['vin']
    }


lambda_handler = recall_get_vehicle
