import logging
import json
import boto3
import base64

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
    }
})


@arcimoto.runtime.handler
def users_user_get(username):
    global logger

    # users are allowed to get their own profile - otherwise need permission
    current_user = arcimoto.user.current()
    if username != current_user.username:
        current_user.assert_permission('users.user.read')

    user = arcimoto.user.User(username)

    if not user.exists:
        raise ArcimotoArgumentError('Invalid username')

    user_profile = user.get_profile()
    preferences = user.get_preferences()
    permissions = user.get_roles()
    user_permission_groups = user.get_groups()
    user_abilities = user.get_abilities()

    # add in the cognito status
    cognito = boto3.client('cognito-idp')
    cognito_response = cognito.admin_get_user(
        UserPoolId=arcimoto.user.USER_POOL_ID,
        Username=username
    )

    # collect all the bits into a single response with sensible defaults
    response = {
        'profile': {
            'username': username,
            'display_name': user_profile.get('display_name', None),
            'avatar': user_profile.get('avatar', None),
            'avatar_file_type': user_profile.get('avatar_file_type', None),
            'phone': user_profile.get('phone', None),
            'email': user_profile.get('email', None)
        },
        'preferences': preferences,
        'permissions': permissions,
        'permission_groups': user_permission_groups,
        'abilities': user_abilities,
        'cognito': {
            'Username': cognito_response.get('Username', None),
            'UserAttributes': cognito_response.get('UserAttributes', []),
            'UserCreateDate': str(cognito_response.get('UserCreateDate', None)),
            'UserLastModifiedDate': str(cognito_response.get('UserLastModifiedDate', None)),
            'Enabled': cognito_response.get('Enabled', False),
            'UserStatus': cognito_response.get('UserStatus', 'INVALID'),
            'MFAOptions': cognito_response.get('MFAOptions', []),
            'PreferredMfaSetting': cognito_response.get('PreferredMfaSetting', None),
            'UserMFASettingList': cognito_response.get('UserMFASettingList', []),
        }
    }

    return response


lambda_handler = users_user_get
