import logging
import json
import boto3

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.vehicle

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
def reef_vehicle_shadow_synchronized(vin):
    vehicle = arcimoto.vehicle.Vehicle(vin)
    if not vehicle.validate_access_reef():
        raise ArcimotoPermissionError(f'Unauthorized: {vin} not controlled by REEF')
    if not vehicle.exists:
        raise ArcimotoNotFoundError(f'Invalid vin: {vin}')

    iot_client = boto3.client('iot-data')
    vehicle_shadow_synchronized = False

    try:
        response = iot_client.get_thing_shadow(
            thingName=vin
        )
        response_payload = response.get('payload', None)
        vehicle_shadow_payload = json.loads(response_payload.read())
        shadow_state = vehicle_shadow_payload.get('state', None)
        if 'delta' not in shadow_state:
            vehicle_shadow_synchronized = True

    except Exception as e:
        raise ArcimotoREEFAlertException(f'Unable to get shadow for {vin}: {e}')

    return {
        'vehicle_synchronized': vehicle_shadow_synchronized
    }


lambda_handler = reef_vehicle_shadow_synchronized
