import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'username': {
        'type': 'string',
        'required': True
    },
    'vehicle_group_id': {
        'type': 'integer',
        'required': True,
        'min': 1
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('fleets.group.write')
@arcimoto.db.transaction
def fleets_vehicle_group_remove_user(username, vehicle_group_id):

    cursor = arcimoto.db.get_cursor()

    if not vehicle_group_user_join_exists(username, vehicle_group_id):
        raise ArcimotoNotFoundError('Invalid vehicle_group to user association, nothing to remove')

    query = (
        'DELETE FROM users_join_vehicle_group '
        'WHERE '
        'username = %s '
        'AND '
        'vehicle_group = %s'
    )
    cursor.execute(query, [username, vehicle_group_id])
    
    try:
        msg_part = f'User removed from fleet id {vehicle_group_id}'
        arcimoto.note.UserNote(
            userId=username,
            message=msg_part,
            tags=['fleets'],
            source=arcimoto.user.current().get_username()
        )
    except Exception as e:
        error_msg = f'Failure to create user note for {username} removal from vehicle group id {vehicle_group_id}: - {e}'
        raise ArcimotoException(error_msg)

    return {}


def vehicle_group_user_join_exists(username, id):
    return arcimoto.db.check_record_exists('users_join_vehicle_group', {'username': username, 'vehicle_group': id})


lambda_handler = fleets_vehicle_group_remove_user
