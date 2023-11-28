import logging
import json
import time
import datetime
import boto3
from botocore.exceptions import ClientError

from arcimoto.exceptions import *
import arcimoto.args
import arcimoto.note
import arcimoto.runtime

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

ALARMS_URL = "https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#alarmsV2:"
ALARMS_URL_BASE = "https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#alarmsV2:alarm/"
CW_ALARM_ADDENDA = {
    "AuthorityManager 4XXError": {
        "Alarm_URL": "AuthorityManager+4XXError",
        "Recommendation": "Check with Authority Manager users to see what trouble they are having with issuing server requests."
    },
    "AuthorityManager 5XXError": {
        "Alarm_URL": "AuthorityManager+5XXError",
        "Recommendation": "Check with the API Gateway about the status of the Authority Manager API.  Also check the Authority Manager logs on CloudWatch."
    },
    "VehicleManager 4XXError": {
        "Alarm_URL": "VehicleManager+4XXError",
        "Recommendation": "Check with Vehicle Manager users to see what trouble they are having with issuing server requests."
    },
    "VehicleManager 5XXError": {
        "Alarm_URL": "VehicleManager+5XXError",
        "Recommendation": "Check with the API Gateway about the status of the Vehicle Manager API."
    },
    "New Firmware Version Hash Set - prod": {
        "Alarm_URL": "New+Firmware+Version+Hash+Set+-+prod",
        "Recommendation": "The firmware will update on the manufacturing line automatically at 2am.  If this is in the middle of the manufacturing day, go update the firmware on the production line."
    },
    "Firmware version vin set failed": {
        "Alarm_URL": "Firmware+version+vin+set+failed",
        "Recommendation": "Please verify the existence and functionality of the vehicle meta table on the RDS 'telemetryam'"
    },
    "Influx csv Backup - Incoming Log Events": {
        "Alarm_URL": "Influx+csv+Backup+-+Incoming+Log+Events",
        "Recommendation": "Please verify that InfluxDB daily backups are being copied successfully to S3."
    },
    "Get Vehicle Shadow - Incoming Log Events": {
        "Alarm_URL": "Get+Vehicle+Shadow+-+Incoming+Log+Events",
        "Recommendation": "Please verify that IoT system is successfully delivering vehicle shadow documents to vehicles."
    },
    "Telemetry Ingest Influx - Incoming Log Events": {
        "Alarm_URL": "Telemetry+Ingest+Influx+-+Incoming+Log+Events",
        "Recommendation": "Please check the CloudWatch Logs for telemetry_vpc_ingest_influx to find out why global telemetry rate has changed."
    },
    "telemetry_vpc_ingest_influx errors": {
        "Alarm_URL": "telemetry_vpc_ingest_influx+errors",
        "Recommendation": "Please check the CloudWatch Logs for telemetry_vpc_ingest_influx to find out why there is such a high rate of ingestion error."
    },
    "EC2 - memory percent used - DEV-InfluxDB": {
        "Alarm_URL": "EC2+-+memory+percent+used+-+DEV-InfluxDB",
        "Recommendation": "Please check the DEV-InfluxDB EC2 to find out why memory usage is so high."
    },
    "EC2 - memory percent used - STAGE-InfluxDB": {
        "Alarm_URL": "EC2+-+memory+percent+used+-+STAGE-InfluxDB",
        "Recommendation": "Please check the STAGE-InfluxDB EC2 to find out why memory usage is so high."
    },
    "EC2 - memory percent used - InfluxDB": {
        "Alarm_URL": "EC2+-+memory+percent+used+-+InfluxDB",
        "Recommendation": "Please check the InfluxDB EC2 to find out why memory usage is so high."
    },
    "EC2 - memory percent used - Grafana": {
        "Alarm_URL": "EC2+-+memory+percent+used+-+Grafana",
        "Recommendation": "Please check the Grafana EC2 to find out why memory usage is so high."
    },
    "EC2 - Disk Percent Used - DEV-InfluxDB": {
        "Alarm_URL": "EC2+-+Disk+Percent+Used+-+DEV-InfluxDB",
        "Recommendation": "Please check the DEV-InfluxDB EC2 to find out why disk usage is so high."
    },
    "EC2 - Disk Percent Used - STAGE-InfluxDB": {
        "Alarm_URL": "EC2+-+Disk+Percent+Used+-+STAGE-InfluxDB",
        "Recommendation": "Please check the STAGE-InfluxDB EC2 to find out why disk usage is so high."
    },
    "EC2 - Disk Percent Used - InfluxDB": {
        "Alarm_URL": "EC2+-+Disk+Percent+Used+-+InfluxDB",
        "Recommendation": "Please check the InfluxDB EC2 to find out why disk usage is so high."
    },
    "EC2 - Disk Percent Used - Grafana": {
        "Alarm_URL": "EC2+-+Disk+Percent+Used+-+Grafana",
        "Recommendation": "Please check the Grafana EC2 to find out why disk usage is so high."
    },
    "(DEV-InfluxDB) StatusCheckFailed_Instance": {
        "Alarm_URL": "(DEV-InfluxDB)+StatusCheckFailed_Instance",
        "Recommendation": "Please check status of DEV-InfluxDB EC2!"
    },
    "(DEV-InfluxDB) StatusCheckFailed_System": {
        "Alarm_URL": "(DEV-InfluxDB)+StatusCheckFailed_System",
        "Recommendation": "Please check status of DEV-InfluxDB EC2!"
    },
    "(STAGE-InfluxDB) StatusCheckFailed_Instance": {
        "Alarm_URL": "(STAGE-InfluxDB)+StatusCheckFailed_Instance",
        "Recommendation": "Please check status of STAGE-InfluxDB EC2!"
    },
    "(STAGE-InfluxDB) StatusCheckFailed_System": {
        "Alarm_URL": "(STAGE-InfluxDB)+StatusCheckFailed_System",
        "Recommendation": "Please check status of STAGE-InfluxDB EC2!"
    },
    "(InfluxDB) StatusCheckFailed_System": {
        "Alarm_URL": "(InfluxDB)+StatusCheckFailed_System",
        "Recommendation": "Please check status of InfluxDB EC2!"
    },
    "(InfluxDB) StatusCheckFailed_Instance": {
        "Alarm_URL": "(InfluxDB)+StatusCheckFailed_Instance",
        "Recommendation": "Please check status of InfluxDB EC2!"
    },
    "(Grafana) StatusCheckFailed_Instance": {
        "Alarm_URL": "(Grafana)+StatusCheckFailed_Instance",
        "Recommendation": "Please check status of Grafana EC2!"
    },
    "(Grafana) StatusCheckFailed_System": {
        "Alarm_URL": "(Grafana)+StatusCheckFailed_System",
        "Recommendation": "Please check status of Grafana EC2!"
    },
    "Telemetry rate ": {
        "Alarm_URL": "Telemetry+rate+",
        "Recommendation": "Please check incoming telemetry messages from vehicle "
    }

}

AWS_HEALTH_NETWORK_EVENTS = {
    'AWS_VPN_REDUNDANCY_LOSS': {
        'notification_level': arcimoto.note.SEVERITY_INFO
    },
    'AWS_ACM_RENEWAL_STATE_CHANGE': {
        'notification_level': arcimoto.note.SEVERITY_INFO
    }
}


@arcimoto.runtime.handler
def slack_notification(records):
    global logger, AWS_HEALTH_NETWORK_EVENTS

    for record in records:
        sns = record.get('Sns', {})

        subject = sns.get('Subject', None)

        # message can be either JSON, a string that can be JSON decoded or a string
        message = sns.get('Message', None)
        if message is None:
            raise ArcimotoAlertException(f'Unable to load JSON from message for slack notification: {record}')

        msg_lines = []
        message_json = None
        source_type = None
        notification_channel = None
        notification_level = None

        if not isinstance(message, str):
            # message is JSON
            message_json = message
        else:
            try:
                # message is JSON in a string
                message_json = json.loads(message)
            except Exception as e:
                # message is string that can't be decoded to JSON
                logger.warn(f'Unable to load JSON from message for slack notification: {message}: {e}')

        if message_json is not None:
            message_source = message_json.get('source', None)
            if message_source == 'aws.health':
                resources = message_json.get('resources', 'Unknown')
                message_detail = message_json.get('detail', {})
                message_event_type_code = message_detail.get('eventTypeCode', 'Unknown')
                # ignore certain events we know we don't care about
                events_to_ignore = []
                if message_event_type_code not in events_to_ignore:
                    if message_event_type_code in AWS_HEALTH_NETWORK_EVENTS.keys():
                        notification_channel = 'network'
                        notification_level = AWS_HEALTH_NETWORK_EVENTS[message_event_type_code]['notification_level']
                    message_start_time = message_detail.get('startTime', 'Unknown')
                    message_event_description = message_detail.get('eventDescription', {})
                    message_event_latest_description = message_event_description[0].get('latestDescription', 'Unavailable')
                    msg_lines.extend([
                        'AWS Health Event',
                        f'Type Code: {message_event_type_code}',
                        f'Resources: {", ".join(resources)}',
                        f'Start time: {message_start_time}',
                        f'Description: {message_event_latest_description}'
                    ])
                    source_type = 'aws_health_event'
                    source = 'https://phd.aws.amazon.com/phd/home#/account/dashboard/open-issues'
            else:
                # cloudwatch alarm
                notification_channel = 'telemetry'
                alarm_name = message_json.get('AlarmName', None)
                alarm_description = message_json.get('AlarmDescription', None)
                if None in [alarm_description, alarm_name]:
                    raise ArcimotoAlertException(f'Unable to get alarm data from message JSON, message: {message}')

                # Build custom per-vehicle messages if necessary
                if 'Telemetry rate ' in alarm_name:
                    vin = alarm_name.split()[2]
                    addenda = CW_ALARM_ADDENDA.get('Telemetry rate ')
                    alarm_URL = ALARMS_URL_BASE + addenda.get('Alarm_URL') + vin
                    recommendation = addenda.get('Recommendation') + vin
                    source_type = 'telemetry_alarm'
                    source = alarm_URL
                else:
                    addenda = CW_ALARM_ADDENDA.get(alarm_name, None)
                    if addenda is not None:
                        alarm_URL = ALARMS_URL_BASE + addenda['Alarm_URL']
                        recommendation = addenda['Recommendation']
                        source_type = 'telemetry_alarm'
                        source = alarm_URL
                    else:
                        # not a telemetry alarm
                        alarm_URL = ALARMS_URL
                        recommendation = f'Remedy the alarm `{alarm_name}` using the included `source` link.'
                        source_type = 'alarm'
                        source = alarm_name

                msg_lines.extend([
                    alarm_name,
                    f'Description: {alarm_description}',
                    f'To Do: {recommendation}'
                ])

        else:
            # handle if message is string that can't be decoded to JSON
            env = arcimoto.runtime.get_env()
            msg_lines.extend([
                subject,
                message
            ])
            source_type = 'lambda'
            source = f'slack_notification:{env}'

        msg = '\n\n'.join(msg_lines)
        severity = arcimoto.note.SEVERITY_ERROR if notification_level is None else notification_level
        try:
            if notification_channel is 'firmware':
                arcimoto.note.FirmwareNotification(
                    message=msg,
                    source=source,
                    source_type=source_type,
                    severity=severity
                )
            elif notification_channel is 'manufacturing':
                arcimoto.note.ManufacturingNotification(
                    message=msg,
                    source=source,
                    source_type=source_type,
                    severity=severity
                )
            elif notification_channel is 'network':
                arcimoto.note.NetworkNotification(
                    message=msg,
                    source=source,
                    source_type=source_type,
                    severity=severity
                )
            elif notification_channel is 'orders':
                arcimoto.note.OrdersNotification(
                    message=msg,
                    source=source,
                    source_type=source_type,
                    severity=severity
                )
            elif notification_channel is 'reef':
                arcimoto.note.REEFNotification(
                    message=msg,
                    source=source,
                    source_type=source_type,
                    severity=severity
                )
            elif notification_channel is 'replicate':
                arcimoto.note.ReplicateNotification(
                    message=msg,
                    source=source,
                    source_type=source_type,
                    severity=severity
                )
            elif notification_channel is 'service':
                arcimoto.note.ServiceNotification(
                    message=msg,
                    source=source,
                    source_type=source_type,
                    severity=severity
                )
            elif notification_channel is 'telemetry':
                arcimoto.note.TelemetryNotification(
                    message=msg,
                    source=source,
                    source_type=source_type,
                    severity=severity
                )
            elif notification_channel is 'yrisk':
                arcimoto.note.YRiskNotification(
                    message=msg,
                    source=source,
                    source_type=source_type,
                    severity=severity
                )
            else:
                arcimoto.note.Notification(
                    message=msg,
                    source=source,
                    source_type=source_type,
                    severity=severity
                )
        except Exception as e:
            raise ArcimotoAlertException(f'Failed to send notification: {e}')

    return {}


lambda_handler = slack_notification
