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
        'required': True,
        'default': '*'
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
@arcimoto.user.require('users.group.remove-permission')
@arcimoto.db.transaction
def users_remove_permission_from_group(permission, resource, group_id):
    global logger

    cursor = arcimoto.db.get_cursor()

    query = (
        'DELETE FROM user_permission_group_join '
        'WHERE permission=%s '
        'AND resource=%s '
        'AND group_id=%s '
    )
    cursor.execute(query, [permission, resource, group_id])

    return {}


lambda_handler = users_remove_permission_from_group
