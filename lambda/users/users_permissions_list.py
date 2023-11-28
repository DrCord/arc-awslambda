import logging
import json

from arcimoto.exceptions import *
import arcimoto.args
import arcimoto.runtime
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
        'nullable': True,
        'default': None
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('users.permissions.read')
def users_permissions_list(group_id=None):
    global logger

    permissions = []

    cursor = arcimoto.db.get_cursor()

    # Profile is top-level data structure
    query = ('SELECT permission, resource, description '
             'FROM user_permission '
             )
    if group_id is not None:
        query += (
            'WHERE permission IN '
            '(SELECT permission '
            'FROM user_permission_group_join '
            'WHERE group_id=%s)'
        )
    cursor.execute(query, [group_id])

    for record in cursor:
        permissions.append(
            {
                'permission': record['permission'],
                'resource': record['resource'],
                'description': record['description']
            }
        )

    return permissions


lambda_handler = users_permissions_list
