import logging
from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db
import arcimoto.vehicle

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def to_bool(v):
    return v.lower() in ('true', '1')


arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    },
    'managed_session_mode': {
        'type': 'boolean',
        'nullable': True,
        'default': False,
        'coerce': (str, to_bool)
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('vehicles.vehicle.provision')
@arcimoto.db.transaction
def managed_session_mode_set(vin, managed_session_mode):
    vehicle = arcimoto.vehicle.Vehicle(vin)
    if not vehicle.exists:
        raise ArcimotoNotFoundError(f'Invalid vin: {vin}')

    if not managed_session_mode:
        query = (
            'DELETE FROM managed_sessions_vehicles '
            'WHERE vin = %s'
        )

    else:
        query = (
            'INSERT INTO managed_sessions_vehicles (vin) '
            'VALUES (%s) '
            'ON CONFLICT DO NOTHING'
        )

    cursor = arcimoto.db.get_cursor()
    try:
        cursor.execute(query, [vin])
    except Exception as e:
        raise ArcimotoException(e)

    return {}


lambda_handler = managed_session_mode_set
