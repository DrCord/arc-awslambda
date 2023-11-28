import logging
import boto3
from botocore.exceptions import ClientError

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

boto = boto3.client('cognito-idp')

arcimoto.args.register({
    'username': {
        'type': 'string',
        'required': True,
        'regex': r'[0-9a-z]{8}-([0-9a-z]{4}-){3}[0-9a-z]{12}'
    }
})


@arcimoto.runtime.handler
def users_user_mfa_totp_enable(username):
    global logger

    # users are allowed to edit their own profile - otherwise need proper permission
    if username != arcimoto.user.current().username:
        arcimoto.user.current().assert_permission('users.user-profile.write')

    try:
        response = cognito_user_mfa_enable_totp(username)
    except Exception as e:
        raise e

    return response


def cognito_user_mfa_enable_totp(username):
    global logger, boto

    try:
        response = boto.admin_set_user_mfa_preference(
            SMSMfaSettings={
                'Enabled': True,
                'PreferredMfa': False
            },
            SoftwareTokenMfaSettings={
                'Enabled': True,
                'PreferredMfa': True
            },
            Username=username,
            UserPoolId=arcimoto.user.USER_POOL_ID
        )
    except ClientError as e:
        # handle when user has not set up software token mfa by returning notice
        if e.response['Error']['Code'] == 'InvalidParameterException':
            return {'response': f'Error: {e.response["Error"]["Message"]}'}
    except Exception as e:
        raise ArcimotoException('Unable to enable MFA using admin_set_user_mfa_preference for cognito user: {}'.format(e))

    return {'response': 'success'}


lambda_handler = users_user_mfa_totp_enable
