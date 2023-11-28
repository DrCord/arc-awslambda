import boto3
import copy
import json
import logging
from dateutil.parser import parse

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args

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
def telemetry_ingest_timestream(records):
    global json

    env = arcimoto.runtime.get_env()
    client = boto3.client('timestream-write')
    request_records = []

    for record in records:
        body = record.get('body', {})
        # handles weird behavior in test cases
        if type(body) == str:
            body = json.loads(body)
        data = body.get('data', None)
        env_prefix = body.get('env_prefix', None)
        vin = body.get('vin', None)

        if data is None:
            raise ArcimotoArgumentError('data missing from event')
        if vin is None:
            raise ArcimotoArgumentError('vin missing from event')

        if env == 'prod' and env_prefix:
            raise ArcimotoArgumentError('Input validation fail: env_prefix == True can not be used in prod')

        if env_prefix:
            if env == 'dev':
                vin_prefixed = 'DEV-' + vin
            elif env == 'staging':
                vin_prefixed = 'STAGE-' + vin

        for item in data:
            json_data = {'vin': vin_prefixed if env_prefix else vin}
            for item_name in item:
                json_data = handle_field(item_name, item[item_name], json_data)

        # don't insert data if only has vin and timestamp, but no real data point(s)
        if len(json_data) > 2:
            records_to_add = timestream_request_records_prepare(json_data)
            for item in records_to_add:
                request_records.append(item)

    # send telemetry
    if len(request_records) > 0:
        timestream_write_records(client, env, request_records)

    return {}


def handle_field(name, field, json_data):
    global logger

    if name == 'gps_position':
        try:
            lat_lon = field.split(',')
            if 'gps_position' not in json_data:
                json_data['gps_position'] = {}
            json_data['gps_position']['gps_latitude'] = float(lat_lon[0])
            json_data['gps_position']['gps_longitude'] = float(lat_lon[1])
        except AttributeError as e:
            logger.warn('GPS position: {}'.format(field))
            logger.warn('GPS position split error: {}'.format(e))
        return json_data
    elif name == 'gps_altitude':
        if 'gps_position' not in json_data:
            json_data['gps_position'] = {}
        json_data['gps_position']['gps_altitude'] = field
        return json_data
    elif name == 'timestamp':
        dateobj = parse(field)
        json_data['timestamp'] = int(round(dateobj.timestamp()))  # POSIX time
        return json_data

    # default is pass through
    json_data[name] = field
    return json_data


def timestream_write_records(client, env, request_records):
    db_name = 'telemetry'
    if env != 'prod':
        db_name = f'telemetry-{env}'
    try:
        client.write_records(
            DatabaseName=db_name,
            TableName='vehicles',
            Records=request_records
        )
    except client.exceptions.RejectedRecordsException as err:
        logger.warn(f'RejectedRecords: {err}')
        for rr in err.response['RejectedRecords']:
            logger.warn('Rejected Index ' + str(rr['RecordIndex']) + ': ' + rr['Reason'])
        logger.warn('Other records were written successfully. ')
    except Exception as err:
        raise ArcimotoTelemetryAlertException(err)


def timestream_request_records_prepare(json_data):
    records = []
    record_template = {
        'Dimensions': [
            {
                'Name': 'vin',
                'Value': json_data.get('vin')
            },
        ],
        'Time': str(json_data.get('timestamp')),
        'TimeUnit': 'SECONDS'
    }
    for item_name in json_data:
        if item_name not in ['vin', 'timestamp']:
            item_data = json_data.get(item_name)
            record = copy.deepcopy(record_template)
            # handle gps
            if item_name == 'gps_position':
                if 'gps_latitude' in item_data and 'gps_longitude' in item_data:
                    record['MeasureValueType'] = 'DOUBLE'
                    record['MeasureName'] = 'lat'
                    record['MeasureValue'] = str(item_data.get('gps_latitude'))
                    records.append(record)

                    record2 = copy.deepcopy(record_template)
                    record2['MeasureValueType'] = 'DOUBLE'
                    record2['MeasureName'] = 'long'
                    record2['MeasureValue'] = str(item_data.get('gps_longitude'))
                    records.append(record2)

                    if 'gps_altitude' in item_data:
                        record3 = copy.deepcopy(record_template)
                        record3['MeasureValueType'] = 'DOUBLE'
                        record3['MeasureName'] = 'gps_altitude'
                        record3['MeasureValue'] = str(item_data.get('gps_altitude'))
                        records.append(record3)
            else:
                # handle Boolean
                if isinstance(item_data, bool):
                    record['MeasureName'] = item_name
                    record['MeasureValue'] = str(item_data)
                    record['MeasureValueType'] = 'BOOLEAN'
                # handle all other values
                else:
                    record['MeasureName'] = item_name
                    record['MeasureValue'] = str(item_data)
                    record['MeasureValueType'] = 'DOUBLE'
                records.append(record)

    return records


lambda_handler = telemetry_ingest_timestream
