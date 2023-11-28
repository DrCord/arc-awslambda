import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

import authorities

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'id': {
        'type': 'integer',
        'required': True,
        'min': 2
    },
    'vin': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('authorities.vehicle.sign')
@arcimoto.db.transaction
def unprovision_vehicle_authority(id, vin):
    global logger

    cursor = arcimoto.db.get_cursor()
    authorities_resources = authorities.Authorities()

    if authorities_resources.authority_exists(id) is False:
        raise ArcimotoNotFoundError('Authority id does not exist')

    if authorities_resources.authority_has_authority_for_vin(id, vin) is False:
        raise ArcimotoArgumentError('Authority id does not control vin')

    query = (
        'DELETE FROM vehicle_authority '
        'WHERE authority_id=%s '
        'AND vin=%s'
    )
    cursor.execute(query, [id, vin])
    if cursor.rowcount > 1:
        raise ArcimotoArgumentError('Unprovision input parameters did not match database authority record')

    return {}


lambda_handler = unprovision_vehicle_authority
