import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'permission': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'resource': {
        'type': 'string',
        'default': '*',
        'required': True,
        'empty': False
    },
    'group': {
        'rename': 'group_id'
    },
    'group_id': {
        'type': 'integer',
        'min': 1,
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('users.group.add-permission')
@arcimoto.db.transaction
def users_add_permission_to_group(permission, resource, group_id):
    global logger

    cursor = arcimoto.db.get_cursor()
    query = (
        'INSERT INTO user_permission_group_join '
        '(permission, resource, group_id) '
        'VALUES (%s, %s, %s) '
        'ON CONFLICT ON CONSTRAINT user_permission_group_join_pkey DO NOTHING'
    )

    cursor.execute(query, [permission, resource, group_id])

    return {}


lambda_handler = users_add_permission_to_group
