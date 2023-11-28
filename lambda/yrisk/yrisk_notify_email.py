import logging
import boto3
from botocore.exceptions import ClientError

from arcimoto.exceptions import *
import arcimoto.runtime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

AWS_REGION = 'us-west-2'

# This address must be verified with Amazon SES.
SENDER = 'Arcimoto Y-Risk Monthly Export Processing <no-reply@arcimoto.com>'


@arcimoto.runtime.handler
def yrisk_notify_email():
    global logger, AWS_REGION, SENDER

    recipient = 'yrisk-monthly-export'

    env = arcimoto.runtime.get_env()
    if env != 'prod':
        recipient += f'-{env}'

    recipient += '@arcimoto.com'

    # The subject line for the email.
    SUBJECT = f'Y-Risk Monthly Vehicles Export Complete'
    if env != 'prod':
        SUBJECT += f' - {env}'

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (
        'Y-Risk Monthly Vehicles Export Completed\r\n'
        'The data exported to Y-Risk for their consumption is available to view on the S3 bucket arcimoto-yrisk.'
    )

    # The HTML body of the email.
    BODY_HTML = f'''<html>
    <head></head>
    <body>
    <h1>Y-Risk Monthly Vehicles Export</h1>
    <p>The data exported to Y-Risk for their consumption is is available to view on the S3 bucket <a href="s3://arcimoto-yrisk/9a4im0t0-36a1-41b5-92a0-ac660f76c37e/">arcimoto-yrisk</a>.</p>
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
        raise ArcimotoYRiskAlertException(e.response['Error']['Message'])
    else:
        return {
            'message_id': response['MessageId']
        }


lambda_handler = yrisk_notify_email
