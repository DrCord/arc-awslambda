import logging
import json
import base64

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'username': {
        'type': 'string',
        'required': True,
        'regex': r'[0-9a-z]{8}-([0-9a-z]{4}-){3}[0-9a-z]{12}'
    }
})


@arcimoto.runtime.handler
def users_profile_get(username):
    global logger

    # users are allowed to get their own profile - otherwise need proper permission
    if username != arcimoto.user.current().username:
        arcimoto.user.current().assert_permission('users.user-profile.read')

    cursor = arcimoto.db.get_cursor()

    query = ('SELECT username, email, phone, display_name, avatar, avatar_file_type '
             'FROM user_profile '
             'WHERE username=%s '
             )
    cursor.execute(query, [username])

    if cursor.rowcount != 1:
        raise ArcimotoNotFoundError('Invalid username, unable to retrieve profile')

    user_profile = cursor.fetchone()

    avatar_bytes = user_profile.get('avatar', None)
    if avatar_bytes is not None:
        avatar = base64.b64encode(avatar_bytes).decode('utf-8')
    else:
        avatar = None

    return {
        'username': user_profile.get('username', None),
        'email': user_profile.get('email', None),
        'display_name': user_profile.get('display_name', None),
        'phone': user_profile.get('phone', None),
        'avatar': avatar
    }


lambda_handler = users_profile_get
