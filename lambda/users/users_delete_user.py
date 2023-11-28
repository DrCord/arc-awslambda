import logging
import boto3

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'username': {
        'type': 'string',
        'required': True,
        'regex': r'[0-9a-z]{8}-([0-9a-z]{4}-){3}[0-9a-z]{12}'
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('users.user.delete')
@arcimoto.db.transaction
def users_delete_user(username):
    global logger

    delete_user_db(username)
    delete_user_cognito(username)

    return {}


def delete_user_db(username):
    cursor = arcimoto.db.get_cursor()

    try:
        query = (
            'DELETE FROM user_group_join '
            'WHERE username=%s'
        )
        cursor.execute(query, [username])

        query = (
            'DELETE FROM user_profile_join_user_preferences '
            'WHERE username=%s'
        )
        cursor.execute(query, [username])

        query = (
            'DELETE FROM user_profile '
            'WHERE username = %s'
        )
        cursor.execute(query, [username])
    except Exception as e:
        raise ArcimotoException('Unable to delete DB user: {}'.format(e))


def delete_user_cognito(username):
    boto = boto3.client('cognito-idp')
    try:
        response = boto.admin_delete_user(
            UserPoolId=arcimoto.user.USER_POOL_ID,
            Username=username
        )
    except Exception as e:
        raise ArcimotoException('Unable to delete cognito user: {}'.format(e))

    return response


lambda_handler = users_delete_user
