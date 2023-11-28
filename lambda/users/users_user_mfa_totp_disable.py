import logging
import boto3

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
def users_user_mfa_totp_disable(username):
    global logger

    # users are allowed to edit their own profile - otherwise need proper permission
    if username != arcimoto.user.current().username:
        arcimoto.user.current().assert_permission('users.user-profile.write')

    try:
        cognito_user_mfa_disable_totp(username)
    except Exception as e:
        raise e

    return {'username': username}


def cognito_user_mfa_disable_totp(username):
    global logger, boto

    env = arcimoto.runtime.get_env()
    if env is arcimoto.runtime.ENV_PROD:
        # if env is prod then force back onto SMS_MFA when disabling TOTP
        try:
            response = boto.admin_set_user_mfa_preference(
                SMSMfaSettings={
                    'Enabled': True,
                    'PreferredMfa': True
                },
                SoftwareTokenMfaSettings={
                    'Enabled': False,
                    'PreferredMfa': False
                },
                Username=username,
                UserPoolId=arcimoto.user.USER_POOL_ID
            )
        except Exception as e:
            raise ArcimotoException('Unable to disable TOTP MFA for cognito user: {}'.format(e))
    else:
        try:
            response = boto.admin_set_user_mfa_preference(
                SoftwareTokenMfaSettings={
                    'Enabled': False,
                    'PreferredMfa': False
                },
                Username=username,
                UserPoolId=arcimoto.user.USER_POOL_ID
            )
        except Exception as e:
            raise ArcimotoException('Unable to disable TOTP MFA for cognito user: {}'.format(e))

    return {'repsonse': 'success'}


lambda_handler = users_user_mfa_totp_disable
