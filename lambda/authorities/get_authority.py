import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'id': {
        'type': 'integer',
        'required': True,
        'min': 1
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('authorities.authority.read')
@arcimoto.db.transaction
def get_vehicle_authority(id):
    global logger

    result = {}

    cursor = arcimoto.db.get_cursor()
    # get the main authority record
    query = (
        'SELECT parent_authority_id, description '
        'FROM authority_keys '
        'WHERE authority_keys_id=%s'
    )
    cursor.execute(query, [id])
    if cursor.rowcount != 1:
        raise ArcimotoArgumentError('Invalid authority id')

    row = cursor.fetchone()
    result['parent'] = row[0]
    result['description'] = row[1]

    # include any direct children
    query = (
        'SELECT authority_keys_id,description '
        'FROM authority_keys '
        'WHERE parent_authority_id=%s '
        'ORDER BY description'
    )
    cursor.execute(query, [id])
    children = []
    for row in cursor:
        child = {
            'id': row[0],
            'description': row[1]
        }
        children.append(child)

    result['children'] = children

    # include all provisioned vehicles
    # TODO this could get large - consider pagination?
    query = (
        'SELECT vin '
        'FROM vehicle_authority '
        'WHERE authority_id=%s '
        'ORDER BY vin'
    )
    cursor.execute(query, [id])
    vehicles = []
    for row in cursor:
        vehicles.append(row[0])

    result['vehicles'] = vehicles

    return result


lambda_handler = get_vehicle_authority
