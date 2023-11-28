import logging
import json
import requests
from dateutil.parser import parse
import boto3

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

TELEGRAF_ENDPOINT = None
ENV = None


@arcimoto.runtime.handler
def telemetry_vpc_ingest_influx(records):
    global logger, json, TELEGRAF_ENDPOINT, ENV

    ENV = arcimoto.runtime.get_env()

    TELEGRAF_ENDPOINT = f'http://{ENV}.influxdb.aws/telegraf'

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    for record in records:
        message_attributes = record.get('attributes', {})
        message_approximate_receive_count = message_attributes.get('ApproximateReceiveCount', 0)
        if int(message_approximate_receive_count) >= 5:
            # delete looping message from queue without re-processing
            message_id = record.get('messageId', None)
            sqs_delete_message(record)
            subject = f'Unable to process message {message_id} with telemetry_vpc_ingest_influx:{ENV}'
            logger.error(f'{subject}: {record}')
            arcimoto_notify(subject, json.dumps(record))
            continue

        body = record.get('body', {})
        # handles weird behavior in test cases
        if type(body) == str:
            body = json.loads(body)
        data = body.get('data', None)
        env_prefix = body.get('env_prefix', None)
        vin = body.get('vin', None)

        if data is None:
            raise ArcimotoArgumentError(f'data missing from event: {body}')
        if vin is None:
            raise ArcimotoArgumentError(f'vin missing from event: {body}')

        if ENV == 'prod' and env_prefix:
            raise ArcimotoArgumentError('Input validation fail: env_prefix == True can not be used in prod')

        # Note: the CloudWatch Metric for vehicle Telemetry rate depends on the VIN
        # appearing in the CloudWatch logs exactly once per run of this function
        logger.info('VIN: {}'.format(vin))

        telegraf_json = []
        for item in data:
            json_data = {'vin': vin}
            for item_name in item:
                item_data = item[item_name]
                if item_data is not None:
                    json_data = handle_field(item_name, item_data, json_data)
                else:
                    logger.warning(f'Unable to get data for {item_name} from {item}.')
            telegraf_json.append(json_data)

        if env_prefix:
            if ENV == 'staging':
                prefix = 'STAGE'
            else:
                prefix = 'DEV'
            for item in telegraf_json:
                item['vin'] = f'{prefix}-{vin}'

        # send telemetry
        response = None
        try:
            response = requests.post(
                TELEGRAF_ENDPOINT,
                data=json.dumps(telegraf_json),
                json=None,
                headers=headers
            )
            response.raise_for_status()
        except Exception as e:
            request_exception_msg = f'Exception encountered posting request to {TELEGRAF_ENDPOINT}. Error: {e}. Payload data: {telegraf_json}'
            raise ArcimotoTelemetryAlertException(request_exception_msg)

    return {}


def handle_field(name, field, json_data):
    if name == 'gps_position':
        try:
            lat_lon = field.split(',')
            json_data['gps_latitude'] = float(lat_lon[0])
            json_data['gps_longitude'] = float(lat_lon[1])
        except AttributeError as e:
            logger.error(f'GPS position split AttributeError. field: {field}, error: {e}')
        return json_data
    elif name == 'timestamp':
        if field is not None:
            try:
                dateobj = parse(field)
            except Exception as e:
                raise ArcimotoTelemetryAlertException(f'Unable to parse field into datetime object. field: {field}, error: {e}')
            json_data['timestamp'] = int(round(dateobj.timestamp() * 1000))  # POSIX time * 1000
            return json_data
        else:
            logger.warning(f'Warning: timestamp Field is None. json_data: {json_data}')
    elif isinstance(field, bool):
        # Convert all boolean values to integers
        # otherwise Telegraf will convert them to strings and throw them out
        field = int(field)

    # default is pass through
    json_data[name] = field
    return json_data


def arcimoto_notify(subject, message_string):
    global ENV

    arcimoto.note.Notification(
        message=subject + '\n\n' + message_string if subject is not None else message_string,
        source=f'telemetry_vpc_ingest_influx:{ENV}',
        source_type='lambda',
        severity='ERROR'
    )


def sqs_delete_message(message):
    global ENV

    sqs_client = boto3.client('sqs')
    queue_url = f'https://sqs.us-west-2.amazonaws.com/511596272857/arcimoto_telemetry_{ENV}'
    message_id = message.get('messageId', None)
    message_receipt_handle = message.get('receiptHandle', None)

    try:
        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message_receipt_handle
        )
    except Exception as e:
        logger.error(f'Exception encountered while attempting to delete unprocessable message {message_id}. Error: {e}, Message: {message}')

    logger.warning(f'Unable to process SQS message {message_id}, message deleted. Message: {message}')


lambda_handler = telemetry_vpc_ingest_influx
