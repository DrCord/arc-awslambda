import logging
import boto3
import json

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
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
def get_telemetry_definition(vin):
    vehicle_instance = arcimoto.vehicle.Vehicle(vin)
    vehicle_data = vehicle_instance.get()

    try:
        # get the desired telemetry defs version from the vehicle store
        version = vehicle_instance.telemetry_version

        # get the requested metrics file from S3
        # - if unable to find a specific version, the latest version is used and stored as current
        client = boto3.client('s3')
        response = None
        if version is None:
            response = client.get_object(
                Bucket='arcimoto-telemetry',
                Key='config/metrics.json'
            )
            logger.warning('No version configured - using latest telemetry definitions')

            version = response.get('VersionId', None)
            if version is not None:
                vehicle_instance.telemetry_version = version
        else:
            response = client.get_object(
                Bucket='arcimoto-telemetry',
                Key='config/metrics.json',
                VersionId=version
            )

        if response is None:
            raise ArcimotoException('Unable to fetch telemetry definitions from S3')

        # insert the version as a top-level element of the returned metric.json
        file_content = response['Body'].read().decode('utf-8')
        file_json = json.loads(file_content)
        file_json['_version'] = version
        file_content = json.dumps(file_json)

        # Publish to MQTT topic
        client = boto3.client('iot-data')
        response = client.publish(
            topic='/vehicles/{}/telemetry/defs'.format(vin),
            payload=file_content
        )

    except Exception as e:
        logger.warning('Failed to update telemetry definitions: {}'.format(e))
        raise e

    return json.loads(file_content)


lambda_handler = get_telemetry_definition
