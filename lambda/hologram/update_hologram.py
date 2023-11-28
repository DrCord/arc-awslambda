import logging
import requests
import boto3
import json

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

URL = 'https://dashboard.hologram.io/api/1/devices'
HEADERS = {'Content-Type': 'application/json'}
ORG_ID = '22560'


@arcimoto.runtime.handler
def update_hologram(records):
    '''
    Update hologram device name to VIN
    Process message from SQS Queue. Async, will not return.
    '''
    global logger

    try:
        api_key = arcimoto.runtime.get_secret('hologram.api')['key']
    except Exception as e:
        raise ArcimotoException('Error getting secret: {}'.format(e))

    for record in records:
        logger.info('--Processing Event--')
        payload = json.loads(record['body'])
        try:
            vin = payload.get('vin', None)
            sim = payload.get('data', {}).get('iccid', None)
        except Exception as e:
            raise ArcimotoArgumentError('Invalid Message Body format: {}'.format(e))

        if vin is None:
            raise ArcimotoArgumentError('VIN missing from event')
        if sim is None:
            raise ArcimotoArgumentError('ICCID missing from event')

        hologram_set_name(vin, sim, api_key)


def hologram_set_name(vin, sim, api_key):
    try:
        name_changed = set_name(vin, sim, api_key)
        return {'Success': name_changed}
    except Exception as e:
        logger.exception('set_hologram_sim_name lambda failed: {}'.format(e))
        raise ArcimotoAlertException('Set Hologram Sim Name failed: {}'.format(e))


def set_name(vin, sim, api_key):
    '''Set the device name in Hologram to the vehicle VIN.'''
    try:
        id = str(get_id(sim, api_key))
        params = {
            'apikey': api_key,
            'orgid': ORG_ID,
        }
        payload = json.dumps({'name': vin})
        response = requests.put(
            URL + '/' + id,
            headers=HEADERS,
            params=params,
            data=payload
        ).json()

        if response['success']:
            logger.info('Sucessfully Updated Name to {}'.format(vin))
            return {'SIM': sim, 'new_name': vin}
        else:
            logger.error('set_name request failed')
            logger.info('error: {}'.format(response['error']))
            raise ArcimotoException(response['error'])

    except Exception as e:
        logger.exception('Failed to get device ID: {}'.format(e))
        raise ArcimotoException(e)


def get_id(sim, api_key):
    '''Return the Hologram ID of the vehicle with the supplied SIM (ICCID) number.'''
    params = {
        'apikey': api_key,
        'orgid': ORG_ID,
        'sim': sim
    }

    response = requests.get(
        URL,
        headers=HEADERS,
        params=params
    ).json()

    if response['success']:
        if len(response['data']):
            id = response['data'][0]['id']
        else:
            raise ArcimotoNotFoundError(f'hologram id not found for sim/iccid {sim}')
        return id
    else:
        raise ArcimotoException(response['error'])


lambda_handler = update_hologram
