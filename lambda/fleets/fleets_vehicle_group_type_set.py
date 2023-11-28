import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vehicle_group_id': {
        'type': 'integer',
        'required': True,
        'min': 1
    },
    'type_id': {
        'type': 'integer',
        'required': True,
        'min': 1,
        'nullable': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('fleets.group.write')
@arcimoto.db.transaction
def fleets_vehicle_group_type_set(vehicle_group_id, type_id):
    global logger

    cursor = arcimoto.db.get_cursor()

    if not vehicle_group_exists(vehicle_group_id):
        raise ArcimotoNotFoundError('Invalid vehicle_group id')

    if type_id is None:
        query = (
            'DELETE FROM vehicle_group_join_vehicle_group_type '
            'WHERE group_id = %s'
        )
        cursor.execute(query, [vehicle_group_id])
    else:
        query = (
            'INSERT INTO vehicle_group_join_vehicle_group_type '
            '(group_id, type_id) VALUES (%s, %s) '
            'ON CONFLICT (group_id) DO UPDATE '
            'SET type_id=excluded.type_id'
        )
        cursor.execute(query, [vehicle_group_id, type_id])

    return {}


def vehicle_group_exists(id):
    return arcimoto.db.check_record_exists('vehicle_group', {'id': id})


lambda_handler = fleets_vehicle_group_type_set
