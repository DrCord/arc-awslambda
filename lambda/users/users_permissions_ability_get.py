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
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('users.abilities.read')
@arcimoto.db.transaction
def users_permissions_ability_get(id):
    global logger

    cursor = arcimoto.db.get_cursor()

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
        'constant': None,
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


lambda_handler = users_permissions_ability_get
