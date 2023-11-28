import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
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
        'min': 2,
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('users.group.delete')
@arcimoto.db.transaction
def users_group_delete(group_id):
    global logger

    cursor = arcimoto.db.get_cursor()

    cursor.execute('DELETE FROM user_permission_group_join WHERE group_id=%s', [group_id])
    cursor.execute('DELETE FROM user_group_join WHERE group_id=%s', [group_id])
    cursor.execute('DELETE FROM user_group WHERE id=%s', [group_id])

    return {}


lambda_handler = users_group_delete
