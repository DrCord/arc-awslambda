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
        'min': 1,
        'nullable': True,
        'default': None
    },
    'recall_id': {
        'type': 'integer',
        'min': 1,
        'dependencies': 'vin',
        'nullable': True,
        'default': None
    },
    'vin': {
        'type': 'string',
        'dependencies': 'recall_id',
        'nullable': True,
        'default': None
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('recalls.vehicle.remove')
@arcimoto.db.transaction
def recall_remove_vehicle(vehicle_recall_id, recall_id, vin):
    global logger

    cursor = arcimoto.db.get_cursor()
    recalls_resources = recalls_class.Recalls()

    if not vehicle_recall_id and (not recall_id or not vin):
        raise ArcimotoArgumentError('Either vehicle_recall_id or recall_id and vin are required.')

    query = (
        'DELETE '
        'FROM vehicle_recalls '
    )
    if vehicle_recall_id is not None:
        if recalls_resources.vehicle_recall_exists(vehicle_recall_id) is False:
            raise ArcimotoArgumentError('vehicle_recall_id {} does not exist'.format(vehicle_recall_id))

        query += (
            'WHERE id = %s '
            'RETURNING id'
        )
        record_to_delete = [vehicle_recall_id]
    else:
        if recalls_resources.recall_exists(recall_id) is False:
            raise ArcimotoArgumentError('recall_id {} does not exist'.format(recall_id))

        if recalls_resources.vehicle_exists(vin) is False:
            raise ArcimotoArgumentError('vin {} does not exist'.format(vin))

        query += (
            'WHERE recall_id = %s '
            'AND vin = %s '
            'RETURNING id'
        )
        record_to_delete = [recall_id, vin]

    cursor.execute(query, record_to_delete)
    result_set = cursor.fetchone()
    vehicle_recall_id = result_set['id'] if result_set is not None else None

    return {'id': vehicle_recall_id}


lambda_handler = recall_remove_vehicle
