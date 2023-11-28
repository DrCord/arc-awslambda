import logging
import json
import boto3

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
def get_vehicle_shadow(vin):
    global logger, boto3

    try:
        # read the full shadow document for the VIN
        client = boto3.client('iot-data')
        response = client.get_thing_shadow(
            thingName=vin
        )
        payload = response['payload'].read().decode('utf-8')
        shadow = json.loads(payload)
    except Exception as e:
        raise ArcimotoNotFoundError('Failed to fetch shadow: {}'.format(e))

    try:
        # extract the desired portion of the document
        desired = shadow['state']['desired']

    except Exception as e:
        raise ArcimotoNotFoundError('No desired section in shadow: '.format(e))

    try:
        # publish the content to the corresponding topic
        response = client.publish(
            topic='/vehicles/{}/shadow/desired'.format(vin),
            payload=json.dumps(desired)
        )
        logger.info('Published desired shadow for {}'.format(vin))
    except Exception as e:
        raise ArcimotoException('Failed to publish desired state to topic: {}'.format(e))


lambda_handler = get_vehicle_shadow
