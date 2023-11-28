import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    }
})

ARCIMOTO_AUTHORITY_ID = 1


@arcimoto.runtime.handler
@arcimoto.user.require('authorities.vehicle.unsign_arcimoto')
@arcimoto.db.transaction
def unprovision_vehicle_arcimoto_authority(vin):
    global logger

    cursor = arcimoto.db.get_cursor()

    query = (
        'DELETE FROM vehicle_authority '
        'WHERE authority_id=%s '
        'AND vin=%s'
    )
    cursor.execute(query, [ARCIMOTO_AUTHORITY_ID, vin])

    return {}


lambda_handler = unprovision_vehicle_arcimoto_authority
