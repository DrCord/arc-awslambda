import logging
import boto3
import json

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
    'reported': {
        'type': 'dict',
        'required': True
    }
})


@arcimoto.runtime.handler
def shadow_reported_state(vin, reported):
    global logger, boto3

    client = boto3.client('iot-data')

    payload_data = {
        'state': {
            'reported': reported
        }
    }

    client.update_thing_shadow(
        thingName=vin,
        payload=json.dumps(payload_data)
    )

    return {}


lambda_handler = shadow_reported_state
