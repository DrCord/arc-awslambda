import boto3
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

USERPOOL_ID = 'us-west-2_DI8y1FVMI'  # TEST
# USERPOOL_ID = 'us-west-2_3x5jXoVFD'  # REAL

# THIS IS SUPER DANGEROUS AS ***update_user_pool*** WILL SET(overwrite) ANY VALUE not provided with it's default
# all the values that we care about not being default that can be set by this API call are hard coded into this file, so is fairly safe to use
# you can use this file to switch the alias attached to the triggers for doing dev work, testing, etc.

client = boto3.client('cognito-idp')

update_response = client.update_user_pool(
    UserPoolId=USERPOOL_ID,
    Policies={
        'PasswordPolicy': {
            'MinimumLength': 8,
            'RequireUppercase': True,
            'RequireLowercase': True,
            'RequireNumbers': True,
            'RequireSymbols': True,
            'TemporaryPasswordValidityDays': 7
        }
    },
    LambdaConfig={
        'CustomMessage': 'arn:aws:lambda:us-west-2:511596272857:function:userpool_trigger_custom_message:prod'
    },
    EmailConfiguration={
        'SourceArn': 'arn:aws:ses:us-west-2:511596272857:identity/no-reply@arcimoto.com',
        'ReplyToEmailAddress': 'no-reply@arcimoto.com',
        'EmailSendingAccount': 'DEVELOPER'
    },
    AdminCreateUserConfig={
        'AllowAdminCreateUserOnly': True,
        'InviteMessageTemplate': {
            'SMSMessage': 'Your username is {username} and temporary password is {####}. ',
            'EmailMessage': 'Your username is {username} and temporary password is {####}. ',
            'EmailSubject': 'Your temporary password'
        }
    }
)
