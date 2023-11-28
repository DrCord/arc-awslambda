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
    'username': {
        'type': 'string',
        'regex': r'[0-9a-z]{8}-([0-9a-z]{4}-){3}[0-9a-z]{12}',
        'nullable': True,
        'empty': True
    }
})


@arcimoto.runtime.handler
def users_preferences_list(username=None):
    global logger

    preferences = []

    cursor = arcimoto.db.get_cursor()

    # Profile is top-level data structure
    query = ('SELECT preference, description '
             'FROM user_preferences'
             )
    if username is not None:
        query += (
            'WHERE username IN '
            '(SELECT username '
            'FROM user_profile_join_user_preferences '
            'WHERE username=%s)'
        )
    cursor.execute(query, [username])

    for record in cursor:
        preferences.append(
            {
                'preference': record['preference'],
                'description': record['description']
            }
        )

    return preferences


lambda_handler = users_preferences_list
