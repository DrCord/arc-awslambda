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
def users_user_mfa_sms_enable(username):
    global logger

    # users are allowed to edit their own profile - otherwise need proper permission
    if username != arcimoto.user.current().username:
        arcimoto.user.current().assert_permission('users.user-profile.write')

    try:
        cognito_user_mfa_enable_sms_deprecated(username)
        cognito_user_mfa_enable_sms(username)
    except Exception as e:
        raise e

    return {'response': 'success'}


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
            Username=username,
            UserPoolId=arcimoto.user.USER_POOL_ID
        )
    except Exception as e:
        raise ArcimotoException('Unable to enable MFA using admin_set_user_mfa_preference for cognito user: {}'.format(e))


def cognito_user_mfa_enable_sms_deprecated(username):
    '''
    Uses admin_set_user_settings, which is deprecated in favor of
    admin_set_user_mfa_preference. However, in the AWS cognito console the MFAOptions (from admin_set_user_settings)
    is displayed and the UserMFASettingList (from admin_set_user_mfa_preference) does not display.
    Since we used to use the deprecated setting and it is the only one that displays in the AWS console,
    we continue to set/unset this; to not be confusing to an AWS console viewer and
    to be backwards compatible with all existing users.
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


lambda_handler = users_user_mfa_sms_enable
