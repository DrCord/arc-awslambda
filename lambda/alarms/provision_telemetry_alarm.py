import logging
import boto3

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


LOG_METRIC_NAMESPACE = 'LogMetrics'
LOG_GROUP_NAME = '/aws/lambda/telemetry_vpc_ingest_influx'

cloudwatch_logs_client = boto3.client('logs')
cloudwatch_client = boto3.resource('cloudwatch')

@arcimoto.runtime.handler
def provision_telemetry_alarm(vin):
    global logger

    env = arcimoto.runtime.get_env()
    logger.debug(f'vin: {vin}')

    # create metric
    try:
        metric_name = f'Telemetry Message Rate for VIN {vin}'
        response = cloudwatch_logs_client.put_metric_filter(
            logGroupName=LOG_GROUP_NAME,
            filterName=f'find VIN {vin}',
            filterPattern="\"{}\"".format(vin),
            metricTransformations=[
                {
                    'metricName': metric_name,
                    'metricNamespace': LOG_METRIC_NAMESPACE,
                    'metricValue': '1',
                    'defaultValue': 0
                },
            ]
        )
        logger.debug(f'Put metric filter: {response}')
    except Exception as e:
        logger.exception(f'put_metric_filter failed: {e}')
        raise Exception(f'put_metric_filter failed: {e}')

    # create alarm
    try:
        metric = cloudwatch_client.Metric(LOG_METRIC_NAMESPACE, metric_name)
        alarm = metric.put_alarm(
            AlarmName=f'Telemetry rate {vin}',
            AlarmDescription=f'Telemetry rate above flip threshold for VIN {vin}',
            ActionsEnabled=True,
            OKActions=[],
            AlarmActions=[
                # 'arn:aws:sns:us-west-2:511596272857:cloudwatch_notification_topic_'+env,
                f'arn:aws:sns:us-west-2:511596272857:flip_telemetry_alarm_topic_{env}',
            ],
            InsufficientDataActions=[],
            Statistic='Sum',
            Period=300,  # 3600,  # seconds
            EvaluationPeriods=5,
            # DatapointsToAlarm=5,
            Threshold=2,  # 30,
            ComparisonOperator='GreaterThanThreshold',
            Tags=[
                {
                    'Key': 'category',
                    'Value': 'Telemetry Rate'
                },
                {
                    'Key': 'environment',
                    'Value': env
                },
                {
                    'Key': 'vin',
                    'Value': vin
                },
                {
                    'Key': 'telemetry rate alarm active',
                    'Value': 'True'
                }
            ]
        )
    except Exception as e:
        logger.exception(f'put_alarm failed: {e}')
        raise Exception(f'put_alarm failed: {e}')

    return {
        'alarm_name': alarm.alarm_name,
        'alarm_description': alarm.alarm_description,
        'alarm_actions': alarm.alarm_actions,
        'alarm_arn': alarm.alarm_arn,
        'metric_name': alarm.metric_name
    }


lambda_handler = provision_telemetry_alarm
