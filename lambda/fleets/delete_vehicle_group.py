import logging


# arcimoto specific imports
from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'group_id': {
        'type': 'integer',
        'required': True,
        'min': 2
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('fleets.group.delete')
@arcimoto.db.transaction
def delete_vehicle_group(group_id):
    global logger

    cursor = arcimoto.db.get_cursor()

    query = (
        'SELECT id '
        'FROM vehicle_group '
        'WHERE id=%s'
    )
    cursor.execute(query, [group_id])
    result = cursor.fetchone()
    if result is None:
        raise ArcimotoNotFoundError('Vehicle group id does not exist')

    # delete record in group table
    query = (
        'DELETE FROM vehicle_group '
        'WHERE id=%s'
    )
    cursor.execute(query, [group_id])

    # delete associations in join table
    query = (
        'DELETE FROM vehicle_join_vehicle_group '
        'WHERE group_id=%s'
    )
    cursor.execute(query, [group_id])

    return {}


lambda_handler = delete_vehicle_group
