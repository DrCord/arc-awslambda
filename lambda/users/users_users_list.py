import logging
import json
import boto3
import base64

from arcimoto.exceptions import *
import arcimoto.args
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'group': {
        'rename': 'group_id'
    },
    'group_id': {
        'type': 'integer',
        'min': 1,
        'nullable': True,
        'default': None
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('users.users.read')
def users_users_list(group_id=None):
    global logger

    users = []

    cursor = arcimoto.db.get_cursor()

    # Profile is top-level data structure
    query = (
        'SELECT username, email, phone, display_name, avatar '
        'FROM user_profile '
    )
    if group_id is not None:
        query += (
            'WHERE username IN '
            '(SELECT username '
            'FROM user_group_join '
            'WHERE group_id=%s)'
        )
    cursor.execute(query, [group_id])

    for record in cursor:
        users.append(
            {
                'username': record['username'],
                'email': record['email'],
                'phone': record['phone'],
                'display_name': record['display_name'],
                'avatar': base64.b64encode(record['avatar']).decode('utf-8') if record['avatar'] is not None else None
            }
        )

    return users


lambda_handler = users_users_list
