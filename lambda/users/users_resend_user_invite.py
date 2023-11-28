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


def cognito_user_email_get(username, boto):
    global logger

    email = None

    try:
        # lookup user, assure exists, get email
        response = boto.admin_get_user(
            UserPoolId=arcimoto.user.USER_POOL_ID,
            Username=username
        )
    except Exception as e:
        raise ArcimotoException(f'Unable to open DB connection: {e}') from e

    user_attributes = response.get('UserAttributes', None)
    if user_attributes is None:
        raise ArcimotoException(f'Invalid response from Cognito: {response}')

    for user_attribute in user_attributes:
        if user_attribute.get('Name') == 'email':
            email = user_attribute.get('Value', None)
            break

    if email is None:
        raise ArcimotoException(f'Could not get email from Cognito response: {response}')

    return email


def cognito_user_resend_invite(email, boto):
    global logger

    try:
        response = boto.admin_create_user(
            UserPoolId=arcimoto.user.USER_POOL_ID,
            Username=email,
            DesiredDeliveryMediums=['EMAIL'],
            MessageAction='RESEND'
        )
    except Exception as e:
        raise ArcimotoException(f'Unable to open DB connection: {e}') from e


@arcimoto.runtime.handler
@arcimoto.user.require('users.user.resend_invite')
def users_resend_user_invite(username):
    global logger

    boto = boto3.client('cognito-idp')

    email = cognito_user_email_get(username, boto)
    cognito_user_resend_invite(email, boto)

    return {
        'message': f'User {username} invitation resent'
    }


lambda_handler = users_resend_user_invite
