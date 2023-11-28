import logging
import json
import requests
from dateutil.parser import parse

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    },
    'data': {
        'type': 'list',
        'empty': False,
        'required': True
    }
})

ENV = None
TELEGRAF_ENDPOINT = None


@arcimoto.runtime.handler
def backfill_ingest_request(vin, data):
    global logger, ENV, TELEGRAF_ENDPOINT

    ENV = arcimoto.runtime.get_env()

    TELEGRAF_ENDPOINT = f'http://{ENV}.influxdb.aws/telegraf'

    handle_data(vin, data)


def handle_data(vin, data):
    global logger, ENV, TELEGRAF_ENDPOINT

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

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # send telemetry
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
        raise ArcimotoServiceAlertException(request_exception_msg)

    return {}


def handle_field(name, field, json_data):
    global logger

    if name == 'gps_position':
        try:
            lat_lon = field.split(',')
            json_data['gps_latitude'] = float(lat_lon[0])
            json_data['gps_longitude'] = float(lat_lon[1])
        except AttributeError as e:
            logger.debug('GPS position: {}'.format(field))
            logger.debug('GPS position split error: {}'.format(e))
        return json_data
    elif name == 'timestamp':
        # replace 60.00 second timesstamps with 59.99 so parse lib doesn't error
        dateobj = parse(field.replace(':60.00', ':59.99'))
        json_data['timestamp'] = int(round(dateobj.timestamp() * 1000))  # POSIX time * 1000
        return json_data
    elif isinstance(field, bool):
        # Convert all boolean values to integers,
        # otherwise Telegraf will convert the value to a string and discard it
        field = int(field)

    # default is pass through
    json_data[name] = field

    return json_data


lambda_handler = backfill_ingest_request
