import logging
import boto3
import json

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.vehicle

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {  # this can be a string or a list of strings
        'required': True
    }
})

METRICS_405_VERSION = 'AsjutNU2.QbEvkFL0K9PHM6ssR4VLjwu'


@arcimoto.runtime.handler
def update_shadow_documents(vin):
    if isinstance(vin, list):
        vins = vin
    else:
        vins = [vin]
    for vin in vins:
        update_shadow_document(vin)

    return {}


def update_shadow_document(vin):
    global logger, boto3, json

    lambda_client = boto3.client('lambda')
    env = arcimoto.runtime.get_env()

    trusted_keys = lambda_client.invoke(
        FunctionName='get_trusted_keys:{}'.format(env),
        InvocationType='RequestResponse',
        Payload=json.dumps({'vin': vin}).encode()
    )

    vehicle_instance = arcimoto.vehicle.Vehicle(vin)

    # get telemetry points
    telemetry_points = vehicle_instance.telemetry_points

    # get telemetry version, if None then use default version and set for the vehicle
    try:
        telemetry_version = vehicle_instance.telemetry_version

    except RuntimeError as e:
        logger.exception('update_shadow_document lambda failed with RuntimeError: {}'.format(e))

    if telemetry_version is None:
        # supply default metrics.json version that should work on 405 board
        # TODO - switch this back to call get_latest_telemetry_version once done with 405 problems
        vehicle_instance.telemetry_version = METRICS_405_VERSION

    # get gps privacy setting
    try:
        record_gps = vehicle_instance.record_gps

    except RuntimeError as e:
        logger.exception('update_shadow_document lambda failed with RuntimeError: {}'.format(e))
        raise ArcimotoNoStepUnrollException(e)

    # update desired thing shadow with no frequency_overrides
    payload_data = {
        'state': {
            'desired': {
                'trusted_keys': json.loads(trusted_keys['Payload'].read()),
                'telemetry_version': telemetry_version,
                'telemetry_points': list(telemetry_points.keys()),
                'frequency_overrides': None,
                'record_gps': record_gps
            }
        }
    }

    # managed session
    try:
        # check if vehicle is managed session mode enabled
        managed_session_mode = vehicle_instance.managed_session_mode
        if managed_session_mode:
            # check if in active managed session
            managed_session_current = vehicle_instance.managed_session_current
            # if in active managed session add managed session pin to payload data
            if managed_session_current is not False:
                managed_session_pin = managed_session_current.get('pin', None)
                if managed_session_pin is not None:
                    payload_data['state']['desired']['managed_pin'] = managed_session_pin
            # set to empty string to generate shadow doc delta if not in active managed session
            else:
                payload_data['state']['desired']['managed_pin'] = ''
    except RuntimeError as e:
        logger.exception('update_shadow_document lambda RuntimeError: {}'.format(e))

    vehicle = vehicle_instance.get()
    vehicle_configuration = vehicle.get('configuration', None)
    if vehicle_configuration is not None:
        for config_point_name, config_point_value in vehicle_configuration.items():
            if config_point_name == 'option_governor_max_speed':
                if vehicle.get('allows_governor', False):
                    payload_data['state']['desired'][config_point_name] = coerce_meta_value(config_point_value)
            else:
                payload_data['state']['desired'][config_point_name] = coerce_meta_value(config_point_value)

    # Initialize iot-data client
    iot_client = boto3.client('iot-data')

    try:
        iot_client.update_thing_shadow(
            thingName=vin,
            payload=json.dumps(payload_data)
        )

    except Exception as e:
        logger.warning('Failed to update thing shadow: {}'.format(e))
        raise ArcimotoException(e)

    return {}


def get_latest_telemetry_version():
    # get the latest metrics file from S3 by not requesting a specific version
    global logger, boto3

    version = None
    try:
        client = boto3.client('s3')
        response = None
        response = client.get_object(
            Bucket='arcimoto-telemetry',
            Key='config/metrics.json'
        )

        if response is None:
            raise ArcimotoException('Unable to fetch latest telemetry definitions from S3')

        version = response.get('VersionId', None)

    except Exception as e:
        logger.warning('Failed to update telemetry definitions: {}'.format(e))
        raise ArcimotoException(e)

    return version


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def coerce_meta_value(value):
    if is_float(value):
        return float(value)
    if is_int(value):
        return int(value)
    return value


lambda_handler = update_shadow_documents
