import logging
import boto3
import json

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'versionId': {
        'type': 'string',
        'rename': 'version'
    },
    'version': {
        'type': 'string'
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('telemetry.metrics.read')
def get_telemetry_metrics_keys(version=None):
    global logger, boto3, json

    client = boto3.client('s3')

    try:
        # get the latest metrics file from S3
        if version is None:
            response = client.get_object(
                Bucket='arcimoto-telemetry',
                Key='config/metrics.json'
            )
            logger.warning('No version specified - using latest telemetry definitions')

        # or get the specific version
        else:
            response = client.get_object(
                Bucket='arcimoto-telemetry',
                Key='config/metrics.json',
                VersionId=version
            )
    except Exception as e:
        raise ArcimotoNotFoundError(f'Unable to fetch telemetry definitions from AWS S3: {e}')

    # retrieve the top-level keys of the returned metrics.json
    file_content = response['Body'].read().decode('utf-8')
    file_json = json.loads(file_content)
    telemetry_points = []
    for key in file_json.keys():
        telemetry_points.append(key)

    return {'telemetry_points': telemetry_points}


lambda_handler = get_telemetry_metrics_keys
