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
@arcimoto.user.require('users.user.enable')
def users_enable_user(username):
    global logger

    boto = boto3.client('cognito-idp')
    response = boto.admin_enable_user(
        UserPoolId=arcimoto.user.USER_POOL_ID,
        Username=username
    )

    return {}


lambda_handler = users_enable_user
