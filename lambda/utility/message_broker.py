import logging
import boto3
import json
import requests

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

LAMBDA_NOTIFICATION_TOPIC = 'arn:aws:sns:us-west-2:511596272857:telematics_errors'

SEVERITY_CRITICAL = 'CRITICAL'
SEVERITY_ERROR = 'ERROR'
SEVERITY_WARNING = 'WARNING'
SEVERITY_INFO = 'INFO'

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
def message_broker(records):
    '''Route and handle notification messages sent from lambdas'''
    for record in records:
        logger.info('--Processing Event--')
        body = record['body']
        # handles weird behavior in test cases
        if type(body) == str:
            body = json.loads(record['body'])
        severity = body.get('severity', None)
        message = body.get('message', None)
        source_type = body.get('source_type', None)
        source = body.get('source', None)
        data = body.get('data', None)
        channel = body.get('channel', None)
        handle_message(severity, message, source_type, source, data, arcimoto.runtime.get_env(), channel)


def handle_message(severity, message, source_type, source, data, env, channel=None):
    # Downgrade severity if not sent from production
    if (severity == SEVERITY_CRITICAL) and (env != 'prod'):
        severity = SEVERITY_ERROR

    # by default, only post to SNS if critical or error.
    if severity in [SEVERITY_CRITICAL, SEVERITY_ERROR]:
        publish_sns(message, source_type, source, severity, data, f'{LAMBDA_NOTIFICATION_TOPIC}_{env}')

    # if note then post note
    note = data.get('note', None)
    if note is not None:
        return post_note(note)
    # otherwise send slack notification
    send_slack_notification(message, source_type, source, severity, env, channel)


def send_slack_notification(message, source_type, source, severity, env, channel=None):
    '''Build and send slack notification'''

    # assemble slack webhook url
    webhook_url = None
    slack_webhooks = arcimoto.runtime.get_secret('slack.api')

    if channel is not None:
        webhook_secret_key = None
        available_channels = [
            'firmware',
            'lambda',
            'manufacturing',
            'network',
            'orders',
            'reef',
            'replicate',
            'service',
            'telemetry',
            'yrisk'
        ]
        try:
            if channel in available_channels:
                webhook_secret_key = ':'.join([f'{channel.capitalize()}_Alerts_{channel}-notifications', env])
                webhook_url = slack_webhooks[webhook_secret_key]
        except KeyError as e:
            # use fallback if key not found in webhooks
            logger.warn(f'KeyError: {webhook_secret_key} not found in slack.api (webhooks) secret data')
            pass
    # default/fallback is lambda-notifications channel set
    if webhook_url is None:
        webhook_url = slack_webhooks[':'.join(['Lambda_Alerts_lambda-notifications', env])]

    # create link to source if possible
    if source != 'UNKNOWN':
        if source_type == 'lambda':
            # Get the name of the lambda and create a link to the aws console
            source_lambda = source.split('/')[-1].split('.')[0]
            aws_link = '<https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions/' + source_lambda + '|' + source_lambda + '>'
        elif source_type == 'state_machine':
            # create a link to the aws console
            aws_link = '<https://us-west-2.console.aws.amazon.com/states/home?region=us-west-2#/statemachines/view/arn:aws:states:us-west-2:511596272857:stateMachine:' + source + '>'
        elif source_type == 'alarm':
            # create a link to the aws console
            aws_link = '<https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#alarmsV2:alarm/' + source + '>'
        elif source_type in ['aws_health_event', 'billing_alarm', 'cost_center', 'telemetry_alarm']:
            # link to the aws console provided by lambda generating notification
            aws_link = source

    # build slack message content
    # reference: https://api.slack.com/reference/surfaces/formatting
    payload = {
        "channel": "lambda-notifications",
        "text": message,
        "blocks": [
            {
                # top info header
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": None
                }
            }
        ]
    }
    if source != 'UNKNOWN':
        linkable_sources = [
            'alarm',
            'aws_health_event',
            'billing_alarm',
            'cost_center',
            'lambda',
            'state_machine',
            'telemetry_alarm'
        ]
        if source_type in linkable_sources:
            payload['blocks'].append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Source: " + aws_link
                    }
                }
            )
        elif source_type == 'note':
            payload['blocks'].append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Source: Arcimoto note"
                    }
                }
            )
    payload['blocks'].append(
        {
            "type": "section",
            "text": {
                    "type": "mrkdwn",
                    "text": message,
            }
        }
    )
    # change slack message icon and message on severity
    if severity == SEVERITY_CRITICAL:
        payload["blocks"][0]["text"]["text"] = ":fire: Code Red! @channel A critical error has occurred. "
    elif severity == SEVERITY_ERROR:
        payload["blocks"][0]["text"]["text"] = ":bangbang: An error has occurred. "
    elif severity == SEVERITY_WARNING:
        payload["blocks"][0]["text"]["text"] = ":warning: An warning has occurred. "
    elif severity == SEVERITY_INFO:
        payload["blocks"][0]["text"]["text"] = ":white_check_mark: A notification has been received"

    r = requests.post(url=webhook_url, data=json.dumps(payload))
    if r.status_code != 200:
        logger.error(f'Failed to send message to Slack Webhook. Error: {r.content}, payload: {payload}')
    else:
        logger.info('Notification published to Arcimoto Slack channel.')


def publish_sns(message, source_type, source, severity, data, topic):
    '''publish message to provided sns topic'''
    payload = {
        'message': message,
        'source_type': source_type,
        'source': source,
        'severity': severity,
        'data': data,
    }
    sns = boto3.client('sns')
    response = sns.publish(
        TopicArn=topic,
        Message=json.dumps(payload)
    )
    logger.info('Published to SNS. \nResponse: {}'.format(response))


def post_note(note):
    return arcimoto.runtime.invoke_lambda('note_create', note)


lambda_handler = message_broker
