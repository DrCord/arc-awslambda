import logging
import base64
import boto3

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
    'email': {
        'type': 'string',
        'regex': r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+[a-zA-Z0-9-.]+',
        'nullable': True,
        'default': None,
        'empty': True
    },
    'phone': {
        'type': 'string',
        'minlength': 12,
        'maxlength': 12,
        'regex': r'^\+1[0-9]{10}$',
        'nullable': True,
        'default': None,
        'empty': True
    },
    'display_name': {
        'type': 'string',
        'minlength': 1,
        'empty': True,
        'nullable': True,
        'default': None
    },
    'avatar': {
        'type': 'string',
        'nullable': True,
        'default': None,
        'empty': True
    },
})


@arcimoto.runtime.handler
@arcimoto.db.transaction
def users_profile_update(username, email, phone, display_name, avatar):
    global logger

    # users are allowed to edit their own profile - otherwise need proper permission
    if username != arcimoto.user.current().username:
        arcimoto.user.current().assert_permission('users.user-profile.write')

    if email is None and phone is None and display_name is None and avatar is None:
        raise ArcimotoArgumentError('You must input a value to update')

    user_update_db(username, email, phone, display_name, avatar)
    user_update_cognito(username, email, phone, display_name)

    return {
        'message': f'user {username} profile updated'
    }


def user_update_db(username, email, phone, display_name, avatar):
    cursor = arcimoto.db.get_cursor()

    query = 'UPDATE user_profile SET '
    update_strings = []
    update_values = []
    if email:
        update_strings.append('email=%s')
        update_values.append(email)
    if phone:
        update_strings.append('phone=%s')
        update_values.append(phone)
    if display_name:
        update_strings.append('display_name=%s')
        update_values.append(display_name)
    if avatar:
        avatar_input_parts = avatar.split(';base64,')
        if len(avatar_input_parts):
            avatar_file_type = avatar_input_parts[0].split('/')[1]
            update_strings.append('avatar_file_type=%s')
            update_values.append(avatar_file_type)
            avatar_image = avatar_input_parts[1]
            update_strings.append('avatar=%s')
            update_values.append(base64.b64decode(avatar_image))
    query += ','.join(update_strings)
    query += ' WHERE username=%s'
    update_values.append(username)

    cursor.execute(query, update_values)


def user_update_cognito(username, email, phone, display_name):
    if phone is not None or email is not None or display_name is not None:
        boto = boto3.client('cognito-idp')

        cognito_data_update_package = []

        if phone:
            cognito_data_update_package.append({
                'Name': 'phone_number',
                'Value': phone
            })

        if email:
            cognito_data_update_package.append({
                'Name': 'email',
                'Value': email
            })

        if display_name:
            cognito_data_update_package.append({
                'Name': 'name',
                'Value': display_name
            })

        response = boto.admin_update_user_attributes(
            UserPoolId=arcimoto.user.USER_POOL_ID,
            Username=username,
            UserAttributes=cognito_data_update_package
        )


lambda_handler = users_profile_update
