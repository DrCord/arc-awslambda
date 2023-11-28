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
    'ability_id': {
        'type': 'integer',
        'min': 1,
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('users.user.write')
@arcimoto.user.require('users.group.write')
@arcimoto.db.transaction
def users_ability_grant(username, ability_id):
    global logger

    cursor = arcimoto.db.get_cursor()

    user = arcimoto.user.User(username)
    if not user.exists:
        raise ArcimotoArgumentError('Invalid username')
    # get all abilities in system with associated permissions
    user_abilities_object = arcimoto.user.Abilities()
    system_abilities = user_abilities_object.get_abilities()
    # get requested ability with permissions
    ability = next((item for item in system_abilities if item['id'] == ability_id), None)
    if ability is None:
        raise ArcimotoException(f'Invalid ability_id input: {ability_id} does not exist.')

    # get user => abilitiies
    user_abilities = user.get_abilities()
    # check if user already has ability
    user_has_ability = next((item for item in user_abilities if item['id'] == ability_id), None)
    if user_has_ability is not None:
        return {}
    # get user permissions
    user_permissions = user.get_roles()
    # compare user permissions to requested ability permissions
    requested_ability_permissions = ability.get('permissions', None)
    if requested_ability_permissions is None:
        return {}
    user_missing_permissions = []
    for permission in requested_ability_permissions:
        if permission not in user_permissions.items():
            user_missing_permissions.append(permission)

    # look for user-specific permission group (named by username)
    permission_groups = []
    try:
        query = (
            'SELECT id '
            'FROM user_group '
            'WHERE name = %s'
        )
        cursor.execute(query, [username])
        result = cursor.fetchone()
    except Exception as e:
        raise ArcimotoException(e)

    permission_group_exists = result is not None
    if permission_group_exists:
        permission_group_id = result.get('id')
    else:
        # if group doesn't exist, create it
        try:
            query = (
                'INSERT INTO user_group '
                '(name, machine_name) VALUES (%s, %s) '
                'RETURNING id'
            )
            cursor.execute(query, [username, username])
            if cursor.rowcount != 1:
                raise ArcimotoException('Invalid group creation')
            permission_group_id = cursor.fetchone()['id']
        except Exception as e:
            raise ArcimotoException(e)
        # add user to group
        try:
            query = (
                'INSERT INTO user_group_join '
                '(username, group_id) values (%s, %s)'
            )
            cursor.execute(query, [username, permission_group_id])

        except Exception as e:
            raise ArcimotoException(e)

    # add needed permissions to group
    for permission in user_missing_permissions:
        try:
            query = (
                'INSERT INTO user_permission_group_join '
                '(permission, resource, group_id) '
                'VALUES (%s, %s, %s) '
                'ON CONFLICT ON CONSTRAINT user_permission_group_join_pkey DO NOTHING'
            )

            cursor.execute(query, [permission.get('permission'), permission.get('resource', '*'), permission_group_id])
        except Exception as e:
            raise ArcimotoException(e)

    return {}


lambda_handler = users_ability_grant
