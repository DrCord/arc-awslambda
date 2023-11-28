import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'id': {
        'type': 'integer',
        'required': True,
        'min': 1
    },
    'ability': {
        'type': 'string',
        'nullable': True,
        'empty': False,
        'default': None
    },
    'constant': {
        'type': 'string',
        'nullable': True,
        'empty': False,
        'default': None
    },
    'description': {
        'type': 'string',
        'nullable': True,
        'empty': False,
        'default': None
    },
    'permissions': {
        'type': 'list',
        'nullable': True,
        'empty': False,
        'default': None
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('users.abilities.update')
@arcimoto.db.transaction
def users_permissions_ability_edit(id, ability, constant, description, permissions):
    global logger

    if ability is None and constant is None and description is None and permissions is None:
        raise ArcimotoArgumentError(f'Invalid input: ability, constant, description or permissions must be supplied to edit the record for {id}')

    cursor = arcimoto.db.get_cursor()

    if ability is not None or description is not None:
        where_predicates = [
            {
                'column': 'id',
                'operator': '=',
                'value': id
            }
        ]
        columns_data = [
            {'ability': ability},
            {'constant': constant},
            {'description': description}
        ]
        cursor.execute(*arcimoto.db.prepare_update_query_and_params('user_ability', where_predicates, columns_data))

    if permissions is not None:
        query = (
            'DELETE FROM user_ability_permission_join '
            'WHERE ability_id = %s'
        )
        cursor.execute(query, [id])
        query = (
            'INSERT INTO user_ability_permission_join '
            '(permission, permission_resource, ability_id) VALUES (%s, %s, %s)'
        )
        # insert permissions list in loop into join table using ability id
        for permission in permissions:
            if isinstance(permission, str):
                permission_name = permission
                permission_resource = '*'
            else:
                permission_name = permission.get('permission', None)
                permission_resource = permission.get('resource', '*')
            if permission_name is not None:
                args = [permission_name, permission_resource, id]
                cursor.execute(query, args)

    query = (
        'SELECT ua.id, ua.ability, ua.constant, ua.description, '
        'pj.permission, pj.permission_resource '
        'FROM user_ability as ua '
        'LEFT JOIN user_ability_permission_join as pj '
        'ON ua.id = pj.ability_id '
        'WHERE ua.id = %s '
        'ORDER BY ua.id ASC'
    )
    cursor.execute(query, [id])
    output = {
        'id': id,
        'ability': None,
        'description': None,
        'permissions': []
    }
    for item in cursor.fetchall():
        output['ability'] = item.get('ability')
        output['constant'] = item.get('constant')
        output['description'] = item.get('description')
        output['permissions'].append({
            'permission': item.get('permission'),
            'permission_resource': item.get('permission_resource')
        })

    return output


lambda_handler = users_permissions_ability_edit
