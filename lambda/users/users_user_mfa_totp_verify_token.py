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
    'access_token': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'user_code': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'friendly_device_name': {
        'type': 'string',
        'required': True,
        'empty': False
    }
})


@arcimoto.runtime.handler
def users_user_mfa_totp_verify_token(access_token, user_code, friendly_device_name):
    '''
    This has no access permission as it uses the access token as input
    which can only be obtained from an authenticated user.
    '''
    global logger

    try:
        response = cognito_user_mfa_totp_verify_token(
            access_token,
            user_code,
            friendly_device_name
        )
    except Exception as e:
        raise e

    return {
        'response': response
    }


def cognito_user_mfa_totp_verify_token(access_token, user_code, friendly_device_name):
    global logger, boto

    try:
        response = boto.verify_software_token(
            AccessToken=access_token,
            UserCode=user_code,
            FriendlyDeviceName=friendly_device_name
        )
        return response
    except boto.exceptions.NotAuthorizedException as e:
        response = e.response
        error = e.response.get('Error', {})
        message = error.get('Message', 'Error')
        code = error.get('Code', 'NotAuthorizedException')
        raise ArcimotoException(f'{code}: {message}')
    except Exception as e:
        raise ArcimotoException('Unable to verify software token for cognito user: {}'.format(e))


lambda_handler = users_user_mfa_totp_verify_token
