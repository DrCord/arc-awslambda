import logging

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
    'preference_identifier': {
        'type': 'string',
        'required': True
    },
    'preference_value': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.db.transaction
def users_add_preference_to_user(username, preference_identifier, preference_value):
    global logger

    # users are allowed to edit their own preferences - otherwise need proper permission
    if username != arcimoto.user.current().username:
        arcimoto.user.current().assert_permission('users.user.write')

    cursor = arcimoto.db.get_cursor()
    try:
        query = (
            'INSERT INTO user_profile_join_user_preferences '
            '(username, preference, value) values (%s, %s, %s) '
            'ON CONFLICT ON CONSTRAINT user_profile_join_user_preferences_pkey DO UPDATE '
            'SET value = excluded.value'
        )
        cursor.execute(query, [username, preference_identifier, preference_value])
    except Exception as e:
        raise ArcimotoException(e)

    return {}


lambda_handler = users_add_preference_to_user
