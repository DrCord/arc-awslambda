import logging
import boto3
import copy
from botocore.exceptions import ClientError

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

AWS_REGION = 'us-west-2'

# This address must be verified with Amazon SES.
SENDER = 'Arcimoto User Accounts <no-reply@arcimoto.com>'


@arcimoto.runtime.handler
def userpool_trigger_custom_message():
    '''
    Lambda is attached to the userpool arcimoto.user.USER_POOL_ID as a cognito trigger

    Cognito triggers have no way to configure lambda alias use in the AWS console
    ./utility/userpool/update_dangerous.py script was used to configure a lambda alias
    a resource policy also had to be manually added to the lambda, example:
    aws lambda add-permission --function-name userpool_trigger_custom_message --action lambda:InvokeFunction --statement-id lambda-invoke-userpool-trigger-custom-message-unaliased --principal cognito-idp.amazonaws.com --output text
    '''

    global logger, AWS_REGION, SENDER

    event = arcimoto.runtime.event()

    payload = copy.deepcopy(event)
    triggerSource = event.get('triggerSource', None)

    if triggerSource == 'CustomMessage_AdminCreateUser':
        username = event.get('userName', None)
        request = event.get('request', {})
        usernameParameter = request.get('usernameParameter', None)
        codeParameter = request.get('codeParameter', None)

        # allow normal execution to continue if we don't have the info we need to process
        if not username or not request:
            return payload

        # get user cognito groups
        client = boto3.client('cognito-idp')
        cognito_response = client.admin_list_groups_for_user(
            Username=username,
            UserPoolId=arcimoto.user.USER_POOL_ID
        )
        cognito_user_groups = [item.get('GroupName') for item in cognito_response.get('Groups', [])]

        # check what ENV user is in (dev/staging/prod)
        user_env = None
        if 'dev' in cognito_user_groups:
            user_env = 'dev'
        elif 'staging' in cognito_user_groups:
            user_env = 'staging'
        elif 'prod' in cognito_user_groups:
            user_env = 'prod'
        else:
            raise ArcimotoException(f'Cognito User {username} not in an ENV group')

        # check if user is in arcimoto group
        user_arcimoto = 'arcimoto' in cognito_user_groups

        if user_arcimoto:
            (
                payload['response']['smsMessage'],
                payload['response']['emailSubject'],
                payload['response']['emailMessage']
            ) = arcimoto_messages_generate(user_env, usernameParameter, codeParameter)
        else:
            (
                payload['response']['smsMessage'],
                payload['response']['emailSubject'],
                payload['response']['emailMessage']
            ) = non_arcimoto_messages_generate(user_env, usernameParameter, codeParameter)

    return payload


def arcimoto_messages_generate(user_env, usernameParameter, codeParameter):
    global logger

    if usernameParameter and codeParameter:
        env_prefix = ''
        if user_env == 'dev':
            env_prefix = 'dev.'
        elif user_env == 'staging':
            env_prefix = 'staging.'
        subject = 'Arcimoto account created: username, temporary password and login link'
        smsMessage = 'Your Arcimoto account username is {username} and temporary password is {####} Complete account setup: ' f'https://{env_prefix}api.arcimoto.com/web/v1/palantir/#/'
        emailMessage = f'''
    Your Arcimoto user account credentials are:<br>
<br>
    username: {usernameParameter}<br>
    temporary password: {codeParameter}<br>
<br>
Complete account setup by logging in to <a href="https://{env_prefix}api.arcimoto.com/web/v1/palantir/#/">Palantir</a> and changing your password:<br>
<br>
Login to activate your account within 6 days. If you do not your temporary password will be invalidated and an administrator will need to resend your invite.
'''

    return (smsMessage, subject, emailMessage)


def non_arcimoto_messages_generate(user_env, usernameParameter, codeParameter):
    global logger

    if usernameParameter and codeParameter:
        subject = 'Arcimoto account created: username, temporary password and instructions'
        smsMessage = 'Your Arcimoto account username is {username} and temporary password is {####}'
        emailMessage = f'''
    Your Arcimoto user account credentials are:<br>
<br>
    username: {usernameParameter}<br>
    temporary password: {codeParameter}<br>
<br>
Complete account setup by logging in to a cognito portal.<br>
<br>
Login to activate your account within 6 days. If you do not your temporary password will be invalidated and an administrator will need to resend your invite.
'''

    return (smsMessage, subject, emailMessage)


lambda_handler = userpool_trigger_custom_message
