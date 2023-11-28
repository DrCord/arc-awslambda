import logging
import boto3
from botocore.exceptions import ClientError

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    },
    'recipient': {
        'type': 'string',
        'required': True
    },
    'file_name': {
        'type': 'string',
        'required': True
    }
})

AWS_REGION = 'us-west-2'

# This address must be verified with Amazon SES.
SENDER = 'Arcimoto Backfill Processing <no-reply@arcimoto.com>'


@arcimoto.runtime.handler
def backfill_notify_failed(vin, recipient, file_name):
    global logger, AWS_REGION, SENDER

    # The subject line for the email.
    SUBJECT = f'Backfill telemetry data request for {vin} with file {file_name} failed'

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ('Backfill Telemetry Data Request Failed\r\n'
                 f'The state machine importing your data encountered an issue with processing file {file_name}. Inquire with support for assistance.'
                 )

    # The HTML body of the email.
    BODY_HTML = f'''<html>
    <head></head>
    <body>
    <h1>Backfill Telemetry Data Request Failed for {vin} with file {file_name}</h1>
    <p>The state machine importing your data encountered an issue with processing file {file_name}. Inquire with support for assistance.</p>
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
        raise ArcimotoException(e.response['Error']['Message'])
    else:
        return {
            'message_id': response['MessageId']
        }


lambda_handler = backfill_notify_failed
