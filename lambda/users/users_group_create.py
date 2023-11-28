import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'name': {
        'type': 'string',
        'required': True,
        'empty': False
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('users.group.create')
@arcimoto.db.transaction
def users_group_create(name, machine_name=None):
    global logger

    cursor = arcimoto.db.get_cursor()

    # removing leading and ending spaces from name
    name = name.strip()
    # make machine friendly machine_name
    if machine_name is None:
        machine_name = name.replace(' ', '_').lower()

    query = (
        'INSERT INTO user_group '
        '(name, machine_name) VALUES (%s, %s) '
        'RETURNING id'
    )
    cursor.execute(query, [name, machine_name])
    if cursor.rowcount != 1:
        raise ArcimotoException('Invalid group creation')
    group_id = cursor.fetchone()['id']

    return {
        'name': name,
        'id': group_id
    }


lambda_handler = users_group_create
