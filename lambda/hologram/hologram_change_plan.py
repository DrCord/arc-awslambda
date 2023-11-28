import logging
import requests
import boto3
from botocore.exceptions import ClientError
import json
import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.note

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

URL = 'https://dashboard.hologram.io/api/1/links/cellular/'
HEADERS = {'Content-Type': 'application/json'}
ORG_ID = '22560'
AWS_REGION = 'us-west-2'


@arcimoto.runtime.handler
def hologram_change_plan(records):
    '''
    Process message from SQS Queue. Async, will not return.
    Changes hologram device_id to plan_id
    '''

    try:
        hologram_api_key = arcimoto.runtime.get_secret('hologram.api')['key']
    except Exception as e:
        raise ArcimotoException('Error getting secret: {}'.format(e))

    for record in records:
        body = record.get('body', {})
        # handles weird behavior in test cases
        if type(body) == str:
            body = json.loads(body)
        device_id = body.get('device', None)  # cellular ID
        plan_id = body.get('plan', None)  # plan ID

        if device_id is None:
            raise ArcimotoArgumentError('Cellular ID missing from event')
        if plan_id is None:
            raise ArcimotoArgumentError('Plan ID missing from event')

        hologram_change_device_plan(device_id, plan_id, hologram_api_key)


def hologram_change_device_plan(device_id, plan_id, api_key):
    try:
        update_plan(device_id, plan_id, api_key)
        msg = f'Hologram Cellular ID {device_id} has been automatically updated to Plan ID: {plan_id}'
        arcimoto.note.Notification(message=msg)
    except Exception as e:
        raise ArcimotoAlertException(f'Failed to update Cellular ID {device_id} to Plan ID: {plan_id} \n Exception: {e}')


def update_plan(device_id, plan_id, key):
    '''
    Updates specified plan_id to specified device_id
    Parameters:
    device_id (int): Cellular ID for Hologram Device
    plan_id (int): Plan ID for Hologram Service Plan
    '''
    params = {
        'apikey': key,
        'orgid': ORG_ID,
    }
    payload = json.dumps({
        'plan': plan_id,
        'zone': 'USA'
    })
    response = requests.post(
        URL + str(device_id) + '/changeplan',
        headers=HEADERS,
        params=params,
        data=payload
    ).json()

    if not response['success']:
        raise ArcimotoException('Error in response: {}'.format(response['error']))


lambda_handler = hologram_change_plan
