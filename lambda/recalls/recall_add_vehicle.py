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
    'recall_id': {
        'type': 'integer',
        'required': True,
        'min': 1
    },
    'service_reference': {
        'type': 'string',
        'required': False,
        'nullable': True
    },
    'vins': {
        'type': 'list',
        'required': True,
        'empty': False
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('recalls.vehicle.add')
@arcimoto.db.transaction
def recall_add_vehicle(recall_id, vins, service_reference=None):
    global logger

    cursor = arcimoto.db.get_cursor()

    recalls_resources = recalls_class.Recalls()

    if recalls_resources.recall_exists(recall_id) is False:
        raise ArcimotoArgumentError('recall_id {} does not exist'.format(recall_id))

    errors = []
    for vin in vins:
        if vehicle_exists(vin) is False:
            errors.append('vin {} does not exist'.format(vin))

        if recalls_resources.vehicle_in_recall(vin, recall_id):
            errors.append('vin {} already exists for recall {}'.format(vin, recall_id))
    if len(errors):
        if len(errors) == 1:
            raise ArcimotoArgumentError(errors[0])
        else:
            msg = "\n" + "\n".join(errors)
            raise ArcimotoArgumentError(f'Errors:{msg}')

    if service_reference is None:
        service_reference = ''

    query = (
        'INSERT INTO vehicle_recalls '
        '(recall_id, service_reference, vin) '
        'VALUES (%s, %s, %s) '
        'ON CONFLICT DO NOTHING '
        'RETURNING id'
    )

    vehicle_recall_ids = []
    for vin in vins:
        args = [recall_id, service_reference, vin]
        cursor.execute(query, args)

        result_set = cursor.fetchone()
        vehicle_recall_id = result_set['id'] if result_set is not None else None
        vehicle_recall_ids.append(vehicle_recall_id)

    return {
        'vehicle_recall_ids': vehicle_recall_ids,
        'vins': vins
    }


def vehicle_exists(vin):
    return arcimoto.db.check_record_exists('vehicle', {'vin': vin})


lambda_handler = recall_add_vehicle
