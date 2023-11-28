import logging
from datetime import datetime
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
    'managed_session_id': {
        'type': 'integer',
        'required': True,
        'min': 1
    }
})

TELEMETRY_DB_NAME = 'amtelemetry'


@arcimoto.runtime.handler
def reef_managed_session_telemetry_get(managed_session_id):
    influx_ip = influx_ip_get()

    cursor = arcimoto.db.get_cursor()
    query = (
        'SELECT vin, initialization, completion '
        'FROM managed_sessions_reef '
        'WHERE id = %s'
    )
    try:
        cursor.execute(query, [managed_session_id])
        result = cursor.fetchone()
        if result is None:
            raise ArcimotoArgumentError(f'Invalid managed session id {managed_session_id}')
        managed_session = {
            'id': managed_session_id,
            'vin': result['vin'],
            'initialization': result['initialization'],
            'completion': result['completion']
        }
    except Exception as e:
        raise ArcimotoREEFAlertException(e)

    vin = managed_session.get('vin', None)
    if vin is None:
        raise ArcimotoREEFAlertException(f'Unable to get vin for managed session {managed_session_id}')
    vehicle = arcimoto.vehicle.Vehicle(vin)
    if not vehicle.validate_access_reef():
        raise ArcimotoPermissionError(f'Unauthorized: vehicle not controlled by REEF')

    try:
        managed_session_start = managed_session.get('initialization', None)
        if managed_session_start is None:
            raise ArcimotoREEFAlertException('Unable to process Managed Session initialization')
        managed_session_start_timestamp = managed_session_start.timestamp()
        start_milliseconds = f'{int(managed_session_start_timestamp * 1000)}ms'
    except Exception as e:
        raise ArcimotoREEFAlertException(f'Unable to process start timestamp: {e}')

    try:
        managed_session_end = managed_session.get('completion', None)
        if managed_session_end is None:
            end_milliseconds = f'{int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)}ms'
        else:
            managed_session_end_timestamp = managed_session.get('completion', None).timestamp()
            end_milliseconds = f'{int(managed_session_end_timestamp * 1000)}ms'
    except Exception as e:
        raise ArcimotoREEFAlertException(f'Unable to process end timestamp: {e}')

    managed_session_telemetry_data = {
        'vin': vin,
        'start': arcimoto.db.datetime_record_output(managed_session_start),
        'end': arcimoto.db.datetime_record_output(managed_session_end) if managed_session_end is not None else 'active'
    }

    try:
        telemetry_points = [
            f'bms_pack_soc[{start_milliseconds}:{end_milliseconds}]',
            f'gps_position[{start_milliseconds}:{end_milliseconds}]',
            f'odometer[{start_milliseconds}:{end_milliseconds}]',
            f'speed[{start_milliseconds}:{end_milliseconds}]'
        ]
    except Exception as e:
        raise ArcimotoREEFAlertException(f'Unable to setup telemetry point managed session period for influx requests: {e}')

    # open influxdb client
    client = InfluxDBClient(host=influx_ip, port=90)
    client.switch_database(TELEMETRY_DB_NAME)

    for telemetry_point in telemetry_points:
        # split into name and period before '['
        telemetry_point_pieces = telemetry_point.split('[', 1)
        telemetry_point_name = escape_literal(telemetry_point_pieces[0])
        telemetry_point_period = telemetry_point_pieces[1][:-1]

        # split period into start and end (format: [start:end])
        telemetry_point_periods = telemetry_point_period.split(':')
        period_start = telemetry_point_periods[0]
        if telemetry_point_periods[1] is '':
            period_end = 'now'
        else:
            period_end = telemetry_point_periods[1]

        period = {
            'start': period_start,
            'end': period_end
        }
        managed_session_telemetry_data[telemetry_point_name] = telemetry_point_get_period(client, vin, telemetry_point_name, period)

    return managed_session_telemetry_data


def telemetry_point_get_period(client, vin, telemetry_point, period):
    # query influxdb for a telemetry point for the period
    start_safe = escape_literal(period.get('start'))
    end_safe = escape_literal(period.get('end'))
    query_end = (
        'AND "vin" = $vin '
        'GROUP BY time(1m) '
        'fill(null)'
    )

    # handle gps_position separately
    if telemetry_point == 'gps_position':
        query = (
            'SELECT mean("gps_latitude") AS "latitude", '
            'mean("gps_longitude") AS "longitude", '
            'mean("gps_altitude") AS "altitude" '
        )
    else:
        telemetry_point_safe = escape_literal(telemetry_point)
        query = f'SELECT mean({telemetry_point_safe}) as {telemetry_point_safe} '

    query = query + 'FROM "telemetry" '

    if end_safe == 'now':
        query = query + (
            f'WHERE time >= now() - {start_safe} '
        )
    else:
        query = query + (
            f'WHERE time >= {start_safe} '
            f'AND time <= {end_safe} '
        )

    query = query + (
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
        raise ArcimotoREEFAlertException(e)

    telemetry_data = []
    points = results.get_points()

    if telemetry_point == 'gps_position':
        for point in points:
            latitude = point.get('latitude', None)
            longitude = point.get('longitude', None)
            altitude = point.get('altitude', None)
            time = point.get('time', None)

            if None not in [latitude, longitude, altitude, time]:
                telemetry_data.append({
                    'latitude': latitude,
                    'longitude': longitude,
                    'altitude': altitude,
                    'time': time
                })
    else:
        for point in points:
            data = point.get(telemetry_point, None)
            time = point.get('time', None)

            if data is not None and time is not None:
                telemetry_data.append({
                    'point': data,
                    'time': time
                })

    # if odometer throw away all but first and last point
    if telemetry_point == 'odometer':
        if len(telemetry_data):
            first_point = telemetry_data[0]
            last_point = telemetry_data[-1]
            telemetry_data = [first_point, last_point]
        else:
            telemetry_data = []

    return telemetry_data


def escape_literal(literal):
    # since influxdb bind_params only works on the where clause we need to do some sql injection protection
    escaped_literal = literal
    # from https://stackoverflow.com/a/23190083/1291935
    # If there's a zero byte (\x00) in the string, truncate the string before the zero byte
    zero_byte_location = escaped_literal.find('\x00')
    if zero_byte_location is not -1:
        escaped_literal = escaped_literal[:zero_byte_location - 1]
    # For every ' in the string, replace it with ''
    escaped_literal = escaped_literal.replace("'", "''")

    return escaped_literal


def influx_ip_get():
    try:
        env = arcimoto.runtime.get_env()
        influx_ip = arcimoto.runtime.get_secret(f'telemetry.influxdb.ip.{env}').get('ip', None)
        if influx_ip is None:
            raise ArcimotoREEFAlertException(f'Unable to get IndluxDB IP for {env}')
        return influx_ip
    except Exception as e:
        raise ArcimotoREEFAlertException(e)


lambda_handler = reef_managed_session_telemetry_get
