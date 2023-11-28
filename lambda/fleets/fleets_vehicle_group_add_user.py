import logging

from arcimoto.exceptions import *
import arcimoto.db
import arcimoto.note
import arcimoto.runtime
import arcimoto.user

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
def fleets_vehicle_group_add_user(username, vehicle_group_id):
    global logger

    cursor = arcimoto.db.get_cursor()

    if not user_exists(username):
        raise ArcimotoNotFoundError('Invalid username')
    if not vehicle_group_exists(vehicle_group_id):
        raise ArcimotoNotFoundError('Invalid vehicle_group id')

    query = (
        'INSERT INTO users_join_vehicle_group '
        '(username, vehicle_group) VALUES (%s, %s) '
        'ON CONFLICT (username, vehicle_group) DO NOTHING'
    )
    cursor.execute(query, [username, vehicle_group_id])
    
    try:
        msg_part = f'User added to fleet id {vehicle_group_id}'
        arcimoto.note.UserNote(
            userId=username,
            message=msg_part,
            tags=['fleets'],
            source=arcimoto.user.current().get_username()
        )
    except Exception as e:
        error_msg = f'Failure to create user note for {username} addition to vehicle group id {vehicle_group_id}: - {e}'
        raise ArcimotoException(error_msg)

    return {}


def user_exists(username):
    return arcimoto.user.User(username).exists


def vehicle_group_exists(id):
    return arcimoto.db.check_record_exists('vehicle_group', {'id': id})


lambda_handler = fleets_vehicle_group_add_user
