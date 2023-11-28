import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'group': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('fleets.group.create')
@arcimoto.db.transaction
def create_vehicle_group(group):
    '''Create vehicle group (fleet) from input str group as fleet name'''
    global logger

    cursor = arcimoto.db.get_cursor()

    query = (
        'INSERT INTO '
        'vehicle_group (name) VALUES (%s) '
        'ON CONFLICT DO NOTHING '
        'RETURNING id'
    )
    cursor.execute(query, [group])
    result_set = cursor.fetchone()
    group_id = result_set['id'] if result_set is not None else None

    return {'id': group_id}


lambda_handler = create_vehicle_group
