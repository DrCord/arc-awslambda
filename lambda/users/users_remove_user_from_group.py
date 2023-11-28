import logging

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
@arcimoto.user.require('users.group.write')
@arcimoto.user.require('users.user.write')
@arcimoto.db.transaction
def remove_user_from_group(username, group_id):
    global logger

    cursor = arcimoto.db.get_cursor()
    query = (
        'DELETE FROM user_group_join '
        'WHERE username=%s '
        'AND group_id=%s'
    )
    cursor.execute(query, [username, group_id])
    return {}


lambda_handler = remove_user_from_group
