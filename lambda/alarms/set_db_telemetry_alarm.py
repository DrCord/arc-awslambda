import logging
import boto3
import json

from arcimoto.exceptions import *
import arcimoto.args
import arcimoto.db
import arcimoto.runtime
import arcimoto.vehicle

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


@arcimoto.runtime.handler
def set_db_telemetry_alarm_handler(records):
    global logger

    for record in records:
        logger.debug(f'record: {record}')
        sns = record.get("Sns", {})
        subject = sns.get("Subject", "no subject")
        message = sns.get("Message", "no message")

        try:
            return set_db_telemetry_alarm(subject, json.loads(message))
        except Exception as e:
            logger.exception(f"set_db_telemetry_alarm lambda failed: {e}")

def set_db_telemetry_alarm(subject, message):
    """
    This should only be run on an already existing vehicle.
    If the vehicle does not exist, throw an error message.
    """
    logger.debug(f'message: {message}')
    try:
        alarm_name = message["AlarmName"]
    except Exception as e:
        raise ArcimotoException(f'Unable to get alarm name from input data: {e}')

    try:
        cloudwatch = boto3.resource('cloudwatch')
        client = boto3.client('cloudwatch')
    except Exception as e:
        logger.exception(f'Unable to make boto3 connections: {e}')

    # get vin from tags
    try:
        alarm = cloudwatch.Alarm(alarm_name)
        logger.debug(f'alarm: {alarm}')
    except Exception as e:
        logger.exception(f'Unable to get alarm from cloudwatch: {e}')

    alarm_arn = message.get('AlarmArn', None)
    if alarm_arn is None:
        logger.exception(f'Unable to AlarmArn from message: {message}')
        return {}

    try:
        tags = client.list_tags_for_resource(ResourceARN=alarm_arn)
        logger.debug(f'tags: {tags}')
    except Exception as e:
        logger.exception(f'Unable to list_tags_for_resource {alarm_arn}: {e}')

    vin = None
    try:
        tag_dict_list = tags.get('Tags', [])
        for dict in tag_dict_list:
            if dict.get('Key') == 'vin':
                vin = dict.get('Value', None)
    except Exception as e:
        logger.exception(f'Unable to process vin from Tags: {e}')

    if vin is None:
        logger.exception(f'Unable to get vin, input message: {message}')
        return {}

    # Instantiate vehicle instance and check if vehicle exists
    try:
        vehicle = arcimoto.vehicle.Vehicle(vin)
    except Exception as e:
        logger.exception(f'Unable to instantiate vehicle instance: {e}')
    if not vehicle.exists:
        logger.exception(f'Invalid vin: {vin}')

    # alarm metadata
    try:
        registration = {
            'telemetry rate': False
        }
        for dict in tag_dict_list:
            if dict["Key"] == "telemetry rate alarm active" and dict["Value"] == "True":
                registration["telemetry rate"] = True
    except Exception as e:
        logger.exception(f'Unable to handle alarm metadata: {e}')

    # update vehicle meta alarms data in DB
    try:
        for key, value in registration.items():
            vehicle.update_meta("alarms", key, value)

        # unprovision cloudwatch alarm
        try:
            arcimoto.runtime.invoke_lambda('unprovision_telemetry_alarm', {"vin": vin})
        except Exception as e:
            logger.exception(f'Failed to unprovision CloudWatch telemetry rate alarm: {e}')

    except Exception as e:
        logger.exception(f"Failed to create telemetry alarm db entry: {e}")

    return {}


lambda_handler = set_db_telemetry_alarm_handler