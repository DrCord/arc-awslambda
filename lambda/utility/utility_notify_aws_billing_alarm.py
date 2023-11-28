
import json
import logging
from arcimoto.exceptions import *
import arcimoto.args
import arcimoto.note
import arcimoto.runtime

ALARMS_URL = 'https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#alarmsV2:'
ALARMS_URL_BASE = 'https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#alarmsV2:alarm/'

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


@arcimoto.runtime.handler
def utility_notify_aws_billing_alarm(records):

    for record in records:
        sns = record.get('Sns', {})
        subject = sns.get('Subject', None)
        message = sns.get('Message', None)
        if message is None:
            raise ArcimotoAlertException(f'AWS Billing Alarm Notification has no message in data: {sns}')

        slack_notification(subject, message)

    return {}

def slack_notification(subject, message_string):

    arcimoto.note.Notification(
            message=subject + '\n\n' + message_string if subject is not None else message_string,
            source='AWS Budgets',
            source_type='billing_alarm',
            severity='WARNING'
        )


lambda_handler = utility_notify_aws_billing_alarm

