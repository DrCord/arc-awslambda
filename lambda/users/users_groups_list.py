import logging
import json

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@arcimoto.runtime.handler
@arcimoto.user.require('users.groups.read')
def users_groups_list():
    global logger

    groups = []

    cursor = arcimoto.db.get_cursor()

    # Profile is top-level data structure
    query = (
        'SELECT id, name '
        'FROM user_group'
    )
    cursor.execute(query)

    for record in cursor:
        groups.append(
            {
                'id': record['id'],
                'name': record['name']
            }
        )

    return groups


lambda_handler = users_groups_list
