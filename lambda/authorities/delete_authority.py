import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

import authorities as authorities_class

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'id': {
        'type': 'integer',
        'required': True,
        'min': 2  # Arcimoto Authority ID 1 cannot be deleted
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('authorities.authority.delete')
@arcimoto.db.transaction
def delete_authority(id):
    global logger

    cursor = arcimoto.db.get_cursor()

    authorities_resources = authorities_class.Authorities()

    if not authorities_resources.authority_exists(id):
        raise ArcimotoNotFoundError('Invalid authority id')

    # call the recursive delete
    (vins, authorities) = recurse_delete(id, cursor)

    # returns a dictionary of everything deleted on success
    return {
        'vin': vins,
        'id': authorities
    }


def recurse_delete(authority_id, cursor):
    vins = []
    authorities = []

    # delete any matching vehicle authority mappings
    query = (
        'DELETE FROM vehicle_authority '
        'WHERE authority_id=%s '
        'RETURNING vin'
    )
    cursor.execute(query, [authority_id])
    for row in cursor:
        vins.append(row[0])

    # delete the requested authority
    query = (
        'DELETE FROM authority_keys '
        'WHERE authority_keys_id = %s '
        'RETURNING authority_keys_id'
    )
    cursor.execute(query, [authority_id])
    for row in cursor:
        authorities.append(row[0])

    # recurse to sub-delegated authorities
    query = (
        'SELECT * '
        'FROM authority_keys '
        'WHERE parent_authority_id=%s'
    )
    cursor.execute(query, [authority_id])
    for row in cursor:
        (sub_vins, sub_authorities) = recurse_delete(row[0], cursor)
        # merge the sub-lists into our list
        for sub_vin in sub_vins:
            if sub_vin not in vins:
                vins.append(sub_vin)
        for sub_authority_id in sub_authorities:
            if sub_authority_id not in authorities:
                authorities.append(sub_authority_id)

    return (vins, authorities)


lambda_handler = delete_authority
