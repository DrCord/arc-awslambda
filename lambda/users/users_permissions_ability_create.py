import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'ability': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'constant': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'description': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'permissions': {
        'type': 'list',
        'required': True,
        'empty': False
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('users.abilities.create')
@arcimoto.db.transaction
def users_permissions_ability_create(ability, constant, description, permissions):
    global logger

    cursor = arcimoto.db.get_cursor()

    query = (
        'INSERT INTO user_ability '
        '(ability, constant, description) VALUES (%s, %s, %s) '
        'RETURNING id'
    )
    cursor.execute(query, [ability, constant, description])
    if cursor.rowcount != 1:
        raise ArcimotoException('Invalid ability creation')
    ability_id = cursor.fetchone()['id']

    query = (
        'INSERT INTO user_ability_permission_join '
        '(permission, permission_resource, ability_id) VALUES (%s, %s, %s)'
    )
    # insert permissions list in loop into join table using ability_id
    for permission in permissions:
        if isinstance(permission, str):
            permission_name = permission
            permission_resource = '*'
        else:
            permission_name = permission.get('permission', None)
            permission_resource = permission.get('resource', '*')
        if permission_name is not None:
            args = [permission_name, permission_resource, ability_id]
            cursor.execute(query, args)

    return {
        'ability': ability,
        'id': ability_id,
        'permissions': permissions
    }


lambda_handler = users_permissions_ability_create
