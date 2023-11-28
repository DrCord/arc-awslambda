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
@arcimoto.user.require('users.abilities.delete')
@arcimoto.db.transaction
def users_permissions_ability_delete(id):
    global logger

    cursor = arcimoto.db.get_cursor()

    query = 'DELETE FROM user_ability_permission_join WHERE ability_id = %s'
    cursor.execute(query, [id])
    query = 'DELETE FROM user_ability WHERE id = %s'
    cursor.execute(query, [id])

    return {}


lambda_handler = users_permissions_ability_delete
