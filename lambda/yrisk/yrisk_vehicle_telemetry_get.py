import logging
from datetime import datetime, timedelta
from influxdb import InfluxDBClient

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db
import arcimoto.vehicle

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True,
        'empty': False
    }
})

TELEMETRY_DB_NAME = 'amtelemetry'


@arcimoto.runtime.handler
def yrisk_vehicle_telemetry_get(vin):
    influx_ip = influx_ip_get()

    try:
        (last_month_start, last_month_end) = get_last_month_timestamps()

        last_month_start_timestamp = last_month_start.timestamp()
        start_milliseconds = f'{int(last_month_start_timestamp * 1000)}ms'

        last_month_end_timestamp = last_month_end.timestamp()
        end_milliseconds = f'{int(last_month_end_timestamp * 1000)}ms'

        telemetry_data = {
            'vin': vin,
            'start': arcimoto.db.datetime_record_output(last_month_start),
            'end': arcimoto.db.datetime_record_output(last_month_end)
        }
    except Exception as e:
        raise ArcimotoYRiskAlertException(f'Unable to setup telemetry point period for influx requests: {e}')

    # open influxdb client
    client = InfluxDBClient(host=influx_ip, port=90)
    client.switch_database(TELEMETRY_DB_NAME)

    period = {
        'start': start_milliseconds,
        'end': end_milliseconds
    }
    telemetry_data['odometer'] = telemetry_point_get_period(client, vin, 'odometer', period)
    if len(telemetry_data.get('odometer', [])) == 0:
        telemetry_data['odometer'] = telemetry_point_get_last_available(client, vin, 'odometer', period.get('end'))

    return telemetry_data


def get_last_month_timestamps():
    try:
        current_month = datetime.now().month
        current_year = datetime.now().year
        this_month_start = datetime(current_year, current_month, 1)

        last_month = current_month - 1 if current_month > 1 else 12
        last_month_year = current_year if current_month > 1 else current_year - 1

        last_month_start = datetime(last_month_year, last_month, 1)
        last_month_end = this_month_start - timedelta(seconds=1)
    except Exception as e:
        raise ArcimotoYRiskAlertException(f'Unable to get last month timestamps: {e}')

    return (last_month_start, last_month_end)


def telemetry_point_get_period(client, vin, telemetry_point, period):
    # query influxdb for a telemetry point for the period
    start = period.get('start')
    end = period.get('end')

    query = (
        f'SELECT mean({telemetry_point}) as {telemetry_point} '
        'FROM "telemetry" '
        f'WHERE time >= {start} '
        f'AND time <= {end} '
        'AND "vin" = $vin '
        'GROUP BY time(1m) '
        'fill(null)'
    )

    try:
        results = client.query(
            query=query,
            bind_params={
                'vin': vin
            }
        )
    except Exception as e:
        raise ArcimotoYRiskAlertException(e)

    telemetry_data = []
    points = results.get_points()

    for point in points:
        data = point.get(telemetry_point, None)
        time = point.get('time', None)

        if data is not None and time is not None:
            telemetry_data.append({
                'point': convert_kilometers_to_miles(data),
                'time': time
            })

    # since odometer throw away all but first and last point
    if len(telemetry_data):
        first_point = telemetry_data[0]
        last_point = telemetry_data[-1]
        telemetry_data = [first_point, last_point]

    return telemetry_data


def telemetry_point_get_last_available(client, vin, telemetry_point, last_available_end):
    query = (
        f'SELECT mean(last_odometer) as {telemetry_point} '
        'FROM "365d"."telemetry" '
        'WHERE "vin" = $vin '
        'GROUP BY * '
        'ORDER BY time DESC '
        'LIMIT 1'
    )
    try:
        results = client.query(
            query=query,
            bind_params={
                'vin': vin
            }
        )
    except Exception as e:
        raise ArcimotoYRiskAlertException(e)

    telemetry_data = []
    points = results.get_points()

    for point in points:
        data = point.get(telemetry_point, None)
        time = point.get('time', None)

        if data is not None and time is not None:
            telemetry_data.append({
                'point': convert_kilometers_to_miles(data),
                'time': time
            })

    return telemetry_data


def convert_kilometers_to_miles(kilometers):
    return kilometers * 0.621371


def influx_ip_get():
    try:
        env = arcimoto.runtime.get_env()
        influx_ip = arcimoto.runtime.get_secret(f'telemetry.influxdb.ip.{env}').get('ip', None)
        if influx_ip is None:
            raise ArcimotoYRiskAlertException(f'Unable to get IndluxDB IP for {env}')
        return influx_ip
    except Exception as e:
        raise ArcimotoYRiskAlertException(e)


lambda_handler = yrisk_vehicle_telemetry_get
