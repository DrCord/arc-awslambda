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
    'access_token': {
        'type': 'string',
        'required': True,
        'empty': False
    }
})


@arcimoto.runtime.handler
def users_user_mfa_totp_associate_token(access_token):
    '''
    This has no access permission as it uses the access token as input
    which can only be obtained from an authenticated user.
    '''
    global logger

    try:
        response = cognito_user_mfa_totp_associate_token(access_token)
    except Exception as e:
        raise e

    return {'secret_code': response.get('SecretCode', None)}


def cognito_user_mfa_totp_associate_token(access_token):
    global logger, boto

    try:
        response = boto.associate_software_token(
            AccessToken=access_token
        )
        return response
    except boto.exceptions.NotAuthorizedException as e:
        response = e.response
        error = e.response.get('Error', {})
        message = error.get('Message', 'Error')
        code = error.get('Code', 'NotAuthorizedException')
        raise ArcimotoException(f'{code}: {message}')
    except Exception as e:
        raise ArcimotoException('Unable to associate software token for cognito user: {}'.format(e))


lambda_handler = users_user_mfa_totp_associate_token
