import copy
import logging
import json
import boto3
from botocore.exceptions import ClientError

from arcimoto.exceptions import *
import arcimoto.runtime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'Records': {
        'rename': 'records'
    },
    'records': {
        'type': 'list',
        'required': True,
        'empty': False
    }
})

AWS_REGION = 'us-west-2'

# This address must be verified with Amazon SES.
SENDER = None


@arcimoto.runtime.handler
def utility_email_alert_error(records):
    global logger, AWS_REGION, SENDER

    sent_messages = []

    for record in records:
        recipient = 'aws-alerts'

        sns = record.get('Sns', {})
        subject = sns.get('Subject', None)

        try:
            # message can be either JSON, a string that can be JSON decoded or a string
            message_data = sns.get('Message', None)
            if message_data is None:
                logger.error(f'Unable to load JSON from message for slack notification: {record}')
                continue

            try:
                message_json = json.loads(message_data)
            except Exception as e:
                # already json
                message_json = message_data
            message = message_json.get('message', None)
            if message is None:
                logger.error(f'Unable to load message from JSON for slack notification: {message_data}')
                continue
        except Exception as e:
            # handle if message is string that can't be decoded to JSON
            logger.error(f'Unable to load data for slack notification: {record}: {e}')

        sns_topic_arn = sns.get('TopicArn', None)
        error_env = None
        if 'prod' in sns_topic_arn:
            error_env = 'prod'
        elif 'staging' in sns_topic_arn:
            error_env = 'staging'
        else:
            error_env = 'dev'

        if error_env != 'prod':
            recipient += f'+{error_env}'
            SENDER = f'Telematics Errors - {error_env} <no-reply@arcimoto.com>'
        else:
            SENDER = 'Telematics Errors <no-reply@arcimoto.com>'

        recipient += '@arcimoto.com'

        # The subject line for the email.
        SUBJECT = subject if subject is not None else f'Telematics Error'
        if error_env != 'prod':
            SUBJECT += f' - {error_env}'

        source_type = message_json.get('source_type', None)
        source = message_json.get('source', None)
        severity = message_json.get('severity', None)
        if None in [source_type, source, severity]:
            logger.warning(f'Unable to get additional information from input data: {message_json}')

        # The email body for recipients with non-HTML email clients.
        BODY_TEXT = (
            'Telematics Error\r\n'
            f'{message}'
        )
        if source_type is not None:
            BODY_TEXT += f'\r\n{source_type}'
        if source is not None:
            BODY_TEXT += f'\r\n{source}'
        if severity is not None:
            BODY_TEXT += f'\r\n{severity}'

        # The HTML body of the email.
        BODY_HTML = f'''<html>
        <head></head>
        <body>
        <h1>Telematics Error - {error_env}</h1>
        <p>{message}</p>
        <ul>
            <li>Source: {source if source is not None else "Unknown"}</li>
            <li>Source Type: {source_type if source_type is not None else "Unknown"}</li>
            <li>Severity: {severity if severity is not None else "Unknown"}</li>
        </ul>
        </body>
        </html>
                    '''

        # The character encoding for the email.
        CHARSET = 'UTF-8'

        # Create a new SES resource and specify a region.
        client = boto3.client('ses', region_name=AWS_REGION)

        # Try to send the email.
        try:
            # Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        recipient,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            logger.error(e.response['Error']['Message'])
        else:
            sent_messages.append({
                'message_id': response['MessageId']
            })

    return {'sent_messages': sent_messages}


lambda_handler = utility_email_alert_error
