import logging
import uuid
import boto3
import psycopg2
from psycopg2 import IntegrityError

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

boto = boto3.client('cognito-idp')

arcimoto.args.register({
    'email': {
        'type': 'string',
        'required': True,
        'regex': r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+[a-zA-Z0-9-.]+'
    },
    'phone': {
        'type': 'string',
        'required': True,
        'minlength': 12,
        'maxlength': 12,
        'regex': r'^\+1[0-9]{10}$'
    },
    'display_name': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'enable_mfa': {
        'type': 'boolean',
        'default': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('users.user.create')
@arcimoto.db.transaction
def create_user(email, phone, display_name, enable_mfa=True):
    global logger

    cursor = arcimoto.db.get_cursor()
    # check if user exists in ENV
    query = (
        'SELECT username '
        'FROM user_profile '
        "WHERE email=%s"
    )
    cursor.execute(query, [email])

    if cursor.rowcount == 1:
        # user exists in current ENV
        username = cursor.fetchone().get('username')
    else:
        # user does not exist in current ENV
        username = cognito_user_create_and_associate(email, phone, display_name)

        if enable_mfa:
            try:
                # we enable mfa both the old and new way as the new way
                # is better but the old way shows up in the AWS console...
                cognito_user_mfa_enable_sms(username)
                cognito_user_mfa_enable_sms_deprecated(username)
            except Exception as e:
                delete_cognito_user(username)
                raise e

        # add to arcimoto internal permission group
        db_add_user_to_group(username, None, 'arcimoto')

    return {'username': username}


def cognito_user_create_and_associate(email, phone, display_name):
    global logger

    cursor = arcimoto.db.get_cursor()

    # we create the cognito user twice, first to get the sub/username without an activation email
    # then the second time to trigger the email to the user for activation
    # this prevents us sending the user an email erroneously if the db insert fails
    username = create_cognito_user(email, phone, display_name, False)

    try:
        # db insert to associate cognito user
        query = (
            'INSERT INTO user_profile '
            '(username, display_name, email, phone) '
            'VALUES (%s, %s, %s, %s)'
        )
        cursor.execute(query, [username, display_name, email, phone])

        # add user to ENV group
        cognito_add_user_to_group(username, arcimoto.runtime.get_env())
        # add user to arcimoto internal group
        cognito_add_user_to_group(username, 'arcimoto')

        # calling create on an already existing user will just send the creation email for us
        username = create_cognito_user(email, phone, display_name, True)

    except (psycopg2.DatabaseError, ArcimotoException) as e:
        logger.warning('Failed to create user: {}'.format(e))
        if username:
            delete_cognito_user(username)
        raise ArcimotoException(e)

    return username


def create_cognito_user(email, phone, name, send_invite):
    global logger, boto

    response = boto.admin_create_user(
        UserPoolId=arcimoto.user.USER_POOL_ID,
        Username=email,
        UserAttributes=[
            {
                'Name': 'name',
                'Value': name
            },
            {
                'Name': 'phone_number',
                'Value': phone
            },
            {
                'Name': 'email',
                'Value': email
            },
            {
                'Name': 'phone_number_verified',
                'Value': 'false'
            },
            {
                'Name': 'email_verified',
                'Value': 'true'
            }
        ],
        DesiredDeliveryMediums=['EMAIL'],
        MessageAction='SUPPRESS' if not send_invite else 'RESEND'
    )

    user = response.get('User', None)
    if user is None:
        raise ArcimotoException('Invalid response from Cognito: {}'.format(response))

    username = user.get('Username', None)
    if username is None:
        raise ArcimotoException('Cognito did not set a username: {}'.format(response))

    return username


def delete_cognito_user(username):
    global logger, boto

    try:
        response = boto.admin_delete_user(
            UserPoolId=arcimoto.user.USER_POOL_ID,
            Username=username
        )
    except Exception as e:
        raise ArcimotoAlertException('Unable to delete cognito user: {}'.format(e))


def cognito_user_mfa_enable_sms(username):
    '''
    this uses admin_set_user_mfa_preference, which is the new way rather
    than admin_set_user_settings. However, in the AWS cognito console the MFAOptions
    from admin_set_user_settings is displayed and the UserMFASettingList
    used by admin_set_user_mfa_preference does not display.
    '''
    global logger, boto

    try:
        response = boto.admin_set_user_mfa_preference(
            SMSMfaSettings={
                'Enabled': True,
                'PreferredMfa': True
            },
            # SoftwareTokenMfaSettings={
            #     'Enabled': True|False,
            #     'PreferredMfa': True|False
            # },
            Username=username,
            UserPoolId=arcimoto.user.USER_POOL_ID
        )
    except Exception as e:
        raise ArcimotoException('Unable to enable MFA using admin_set_user_mfa_preference for cognito user: {}'.format(e))


def cognito_user_mfa_enable_sms_deprecated(username):
    '''
    this uses admin_set_user_settings, which is deprecated in favor of
    admin_set_user_mfa_preference. However, in the AWS cognito console the MFAOptions is displayed
    and the UserMFASettingList used by admin_set_user_mfa_preference does not display.
    '''
    global logger, boto

    try:
        response = boto.admin_set_user_settings(
            MFAOptions=[
                {
                    'DeliveryMedium': 'SMS',
                    'AttributeName': 'phone_number'
                },
            ],
            Username=username,
            UserPoolId=arcimoto.user.USER_POOL_ID
        )
    except Exception as e:
        raise ArcimotoException('Unable to enable MFA using admin_set_user_settings for cognito user: {}'.format(e))


def cognito_add_user_to_group(username, group_name):
    global logger, boto

    try:
        response = boto.admin_add_user_to_group(
            UserPoolId=arcimoto.user.USER_POOL_ID,
            Username=username,
            GroupName=group_name
        )
    except Exception as e:
        raise ArcimotoException(f'Unable to add user {username} to Cognito group {group_name} for userpool {arcimoto.user.USER_POOL_ID}. Error: {e}')


def db_add_user_to_group(username, group_id, group_machine_name=None):
    global logger

    cursor = arcimoto.db.get_cursor()
    if group_id is None and group_machine_name is not None:
        # lookup group_id from group_name, proceed
        try:
            query = (
                'SELECT id FROM user_group '
                'WHERE machine_name = %s'
            )
            cursor.execute(query, [group_machine_name])
            if cursor.rowcount != 1:
                raise ArcimotoException('Invalid permission group machine_name')
            group_id = cursor.fetchone().get('id', None)
            if group_id is None:
                raise ArcimotoException('Invalid permission group machine_name')

        except Exception as e:
            raise ArcimotoException(e)

    try:
        query = (
            'INSERT INTO user_group_join '
            '(username, group_id) values (%s, %s)'
        )
        cursor.execute(query, [username, group_id])

    except IntegrityError as e:
        # duplicate insert errors are allowed - catch and ignore
        logger.info(f'User {username} is already a member of group id {group_id} - ignoring')

    except Exception as e:
        raise ArcimotoException(e)


lambda_handler = create_user
