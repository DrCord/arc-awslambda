import logging
from psycopg2 import IntegrityError

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
@arcimoto.user.require('users.user.write')
@arcimoto.user.require('users.group.write')
@arcimoto.db.transaction
def users_add_user_to_group(username, group_id):
    global logger

    cursor = arcimoto.db.get_cursor()
    # duplicate insert errors are allowed - catch and ignore
    try:
        query = (
            'INSERT INTO user_group_join '
            '(username, group_id) values (%s, %s)'
        )
        cursor.execute(query, [username, group_id])

    except IntegrityError as e:
        logger.info(f'User {username} is already a member of group id {group_id} - ignoring')

    return {}


lambda_handler = users_add_user_to_group
