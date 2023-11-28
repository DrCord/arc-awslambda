import logging
import datetime
import json
import boto3
import requests
from botocore.exceptions import ClientError

import arcimoto.runtime
from arcimoto.exceptions import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

URL = 'https://dashboard.hologram.io/api/1/devices'
HEADERS = {'Content-Type': 'application/json'}
ORG_ID = '22560'
HOLOGRAM_DEFAULT_PLAN_ID = 204  # plan 204 - '250MB US Only (T-Mobile)'


@arcimoto.runtime.handler
def hologram_check_plans():
    '''Check for plans that 'expire' within a day, post these to SQS queue'''
    env = arcimoto.runtime.get_env()
    try:
        api_key = arcimoto.runtime.get_secret('hologram.api')['key']
    except Exception as e:
        raise ArcimotoException('Error getting secret: {}'.format(e))

    try:
        to_update = check_plans(api_key)
    except Exception as e:
        raise ArcimotoException('Failed to check plans: {}'.format(e))

    if len(to_update):
        try:
            post_messages(env, to_update)
            # return empty dictionary if successful
            return {}
        except Exception as e:
            raise ArcimotoException('Failed to post to queue: {}'.format(e))


def check_plans(key):
    '''Returns list of device IDs that are one day away from expiring'''
    devices = []
    params = {
        'apikey': key,
        'orgid': ORG_ID,
        'limit': 1000
    }
    response = requests.get(
        URL,
        headers=HEADERS,
        params=params
    ).json()

    if response['success']:
        for device in response['data']:
            # handles (observed) rare case where a device is connecting for the first time.
            if (device['links']['cellular'][0]['whenexpires'] != '0000-00-00 00:00:00') and ('lastsession' in device):
                if device['links']['cellular'][0]['plan']['id'] != HOLOGRAM_DEFAULT_PLAN_ID:
                    expires = device['links']['cellular'][0]['whenexpires']
                    expires_date = datetime.datetime.strptime(expires, '%Y-%m-%d %H:%M:%S')
                    tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1)
                    if expires_date < tomorrow:
                        devices.append(device['links']['cellular'][0]['id'])
                        logger.info(f"Device {device['name']}, needs to change plan")
        return devices
    else:
        raise ArcimotoException(response['error'])


def post_messages(env, content):
    '''Post device cells IDs to SQS queue'''
    sqs = boto3.resource('sqs')
    queue_name = f'hologram_change_plan_{env}'
    logger.info(f'Attemping to add to queue: {queue_name}')
    try:
        queue = sqs.get_queue_by_name(QueueName=queue_name)
    except ClientError as e:
        raise ArcimotoException(e)

    for device in content:
        payload = {
            'device': device,
            'plan': HOLOGRAM_DEFAULT_PLAN_ID
        }
        queue.send_message(MessageBody=json.dumps(payload))
        logger.info(f'posted {payload} to {queue}')


lambda_handler = hologram_check_plans
