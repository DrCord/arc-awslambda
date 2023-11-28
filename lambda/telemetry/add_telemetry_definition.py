import logging
import boto3
import json

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'metrics': {
        'type': 'dict',
        'required': True,
        'empty': False
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('telemetry.definition.write')
@arcimoto.db.transaction
def add_telemetry_definition(metrics):
    global logger, boto3, json

    if arcimoto.runtime.get_env() == 'prod':
        try:
            client = boto3.client('s3')
            response = None
            response = client.put_object(
                Bucket='arcimoto-telemetry',
                Key='config/metrics.json',
                Body=json.dumps(metrics)
            )

            if response is None:
                raise ArcimotoException('Unable to put telemetry definitions into S3 bucket')

            version = response.get('VersionId', None)

        except Exception as e:
            logger.warning(f'Failed to add telemetry definitions to s3 bucket. Exception: {e}')
            raise ArcimotoTelemetryAlertException(f'Failed to add telemetry definitions to s3 bucket. Exception: {e}')
        else:
            return version
    else:
        logger.warning('Error: can only set telemetry definitions in prod environment.')
        raise ArcimotoException('Can only set telemetry definitions in prod environment.')

    return {}


lambda_handler = add_telemetry_definition
