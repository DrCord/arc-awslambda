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
        'required': True
    },
    'vin': {
        'type': 'string',
        'required': True
    }
})

ARCIMOTO_AUTHORITY_ID = 1


@arcimoto.runtime.handler
@arcimoto.user.require('authorities.vehicle.sign')
@arcimoto.db.transaction
def provision_vehicle_authority(id, vin):
    global logger
    global ARCIMOTO_AUTHORITY_ID

    cursor = arcimoto.db.get_cursor()
    authorities_resources = authorities.Authorities()

    # check that the authority exists and get the parent_id back
    query = (
        'SELECT parent_authority_id '
        'FROM authority_keys '
        'WHERE authority_keys_id=%s'
    )
    cursor.execute(query, [id])
    if cursor.rowcount != 1:
        raise ArcimotoNotFoundError('Authority id does not exist')
    parent_id = cursor.fetchone()[0]

    # if the target authority isn't arcimoto, ensure that the vin has already been provisioned
    # to the parent authority (no delegation skipping)
    if id != ARCIMOTO_AUTHORITY_ID:
        if authorities_resources.authority_has_authority_for_vin(parent_id, vin) is False:
            raise ArcimotoArgumentError(f'Authority parent id {parent_id} does not control vin')

    if not authorities_resources.authority_has_authority_for_vin(id, vin):
        # if not already mapped, create the mapping
        query = (
            'INSERT INTO vehicle_authority '
            '(authority_id, vin) values (%s,%s)'
        )
        cursor.execute(query, (id, vin))
    # already existing mappings are not treated as an error

    return {}


lambda_handler = provision_vehicle_authority
