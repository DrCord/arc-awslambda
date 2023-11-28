import boto3
import logging

from arcimoto.exceptions import *
import arcimoto.runtime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True,
        'empty': False
    }
})

cloudwatch_logs_client = boto3.client('logs')
cloudwatch_client = boto3.client('cloudwatch')

LOG_GROUP_NAME = '/aws/lambda/telemetry_vpc_ingest_influx'


@arcimoto.runtime.handler
def unprovision_telemetry_alarm(vin):
    global logger
    
    logger.debug('vin: {}'.format(vin))

    try:
        # remove alarm
        cloudwatch_client.delete_alarms(
            AlarmNames=[
                'Telemetry rate {}'.format(vin),
            ]
        )
    except Exception as e:
        logger.exception(f'unprovision_telemetry_alarm lambda failed to remove alarm: {e}')
        raise Exception(f'Unprovision Telemetry Alarm failed to remove alarm: {e}')

    try:
        # remove metric
        cloudwatch_logs_client.delete_metric_filter(
            logGroupName=LOG_GROUP_NAME,
            filterName='find VIN {}'.format(vin)
        )
    except Exception as e:
        logger.exception(f'unprovision_telemetry_alarm lambda failed to remove metric filter: {e}')
        raise Exception(f'Unprovision Telemetry Alarm failed to remove metric filter: {e}')

    return {}


lambda_handler = unprovision_telemetry_alarm
