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
    'vin': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('authorities.vehicle.read')
@arcimoto.db.transaction
def authkey_vehicle_get(vin):
    global logger

    cursor = arcimoto.db.get_cursor()
    authorities_resources = authorities.Authorities()

    if authorities_resources.vehicle_exists(vin) is False:
        raise ArcimotoNotFoundError('vin does not exist')

    # setup return data structure
    vehicle_info = {
        'authorities': [],
        'pin': {
            'factory_pin': None
        }
    }
    # get authorities info for vin
    query = (
        'SELECT a.authority_keys_id, a.description '
        'FROM authority_keys a '
        'LEFT JOIN vehicle_authority v '
        'ON a.authority_keys_id=v.authority_id '
        'WHERE v.vin=%s'
    )
    cursor.execute(query, [vin])

    for row in cursor:
        authority = {
            'id': row[0],
            'description': row[1]
        }
        vehicle_info['authorities'].append(authority)

    # return all of meta for the vin including the factory_pin
    query = (
        'SELECT value, section, key '
        'FROM vehicle_meta '
        'WHERE vin=%s '
    )
    cursor.execute(query, [vin])
    vin_meta = cursor.fetchall()
    for meta_item in vin_meta:
        vehicle_info[meta_item['section']] = {
            meta_item['key']: meta_item['value']
        }

    return vehicle_info


lambda_handler = authkey_vehicle_get
