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
        'min': 1,
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('users.group.read')
@arcimoto.db.transaction
def users_group_get(group_id):
    global logger

    cursor = arcimoto.db.get_cursor()
    query = (
        'SELECT name '
        'FROM user_group '
        'WHERE id=%s'
    )
    cursor.execute(query, [group_id])
    if cursor.rowcount != 1:
        raise ArcimotoArgumentError('Invalid group selection')
    group_result = cursor.fetchone()

    response = {
        'group_id': group_id,
        'name': group_result.get('name', ''),
        'permissions': [],
        'users': []
    }

    query = ('SELECT p.permission AS permission, '
             'p.resource AS resource, '
             'p.description AS description FROM '
             'user_permission_group_join AS j '
             'LEFT JOIN user_permission AS p '
             'ON j.permission=p.permission '
             'WHERE j.group_id=%s'
             )
    cursor.execute(query, [group_id])
    for row in cursor:
        response['permissions'].append({
            'permission': row['permission'],
            'description': row['description'],
            'resource': row['resource']
        })

    query = (
        'SELECT username '
        'FROM user_group_join '
        'WHERE group_id=%s'
    )
    cursor.execute(query, [group_id])
    for row in cursor:
        response['users'].append(row['username'])

    return response


lambda_handler = users_group_get
