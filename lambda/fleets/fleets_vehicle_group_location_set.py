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
    'location_id': {
        'type': 'integer',
        'required': True,
        'min': 1,
        'nullable': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('fleets.group.write')
@arcimoto.db.transaction
def fleets_vehicle_group_location_set(vehicle_group_id, location_id):
    global logger

    cursor = arcimoto.db.get_cursor()

    if not vehicle_group_exists(vehicle_group_id):
        raise ArcimotoNotFoundError('Invalid vehicle_group id')

    if location_id is None:
        query = (
            'DELETE FROM vehicle_group_join_locations '
            'WHERE group_id = %s'
        )
        cursor.execute(query, [vehicle_group_id])
    else:
        query = (
            'INSERT INTO vehicle_group_join_locations '
            '(group_id, location_id) VALUES (%s, %s) '
            'ON CONFLICT (group_id) DO UPDATE '
            'SET location_id=excluded.location_id'
        )
        cursor.execute(query, [vehicle_group_id, location_id])

    return {}


def vehicle_group_exists(id):
    return arcimoto.db.check_record_exists('vehicle_group', {'id': id})


lambda_handler = fleets_vehicle_group_location_set
