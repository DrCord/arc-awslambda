import logging
import json
from datetime import datetime, timedelta
from influxdb import InfluxDBClient
from psycopg2 import sql

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db
import arcimoto.vehicle

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vins': {
        'type': 'list',
        'default': []
    },
    'telemetry_points': {
        'type': 'list',
        'default': []
    },
    'params': {
        'type': 'dict',
        'default': {}
    }
})

TELEMETRY_DB_NAME = 'amtelemetry'


@arcimoto.runtime.handler
def vehicles_telemetry_get(vins, telemetry_points, params):
    global logger

    user = arcimoto.user.current()
    if not user.authenticated:
        raise ArcimotoPermissionError('Unauthorized telemetry request by guest')

    # get data from querystring if not available directly in the event
    # only overwrites vins or telemetry points from params if they are None
    if not vins or not telemetry_points:
        (vins, telemetry_points) = query_string_get_parameters(params, vins, telemetry_points)

    validate_vins_exist(vins)
    validate_user_has_vins_access(user, set(vins))

    vehicles_telemetry_points = telemetry_points_get_data_for_vins(telemetry_points, vins)

    return {
        'vehicles_telemetry_points': vehicles_telemetry_points
    }


def telemetry_points_get_data_for_vins(telemetry_points, vins):
    client = influx_connect_and_prepare_client()
    vehicles_telemetry_points = {}
    for telemetry_point in telemetry_points:
        (telemetry_point_name, telemetry_point_period) = telemetry_point_parse_input(telemetry_point)

        for vin in vins:
            try:
                vin_in_dict = vehicles_telemetry_points[vin]
            except Exception:
                # vin doesn't exist in vehicles_telemetry_points, create
                vehicles_telemetry_points[vin] = {}
            # latest
            if telemetry_point_period is None:
                vehicles_telemetry_points[vin][telemetry_point_name] = telemetry_point_get_latest(client, vin, telemetry_point_name)
                continue

            # has period with start and end
            period = telemetry_point_parse_period(telemetry_point_period)
            vehicles_telemetry_points[vin][telemetry_point_name] = telemetry_point_get_period(client, vin, telemetry_point_name, period)

    return vehicles_telemetry_points


def validate_vins_exist(vins):
    for vin in vins:
        vehicle_instance = arcimoto.vehicle.Vehicle(vin)
        if not vehicle_instance.exists:
            raise ArcimotoNotFoundError(f'VIN {vin} does not exist.')


def query_string_get_parameters(params, vins, telemetry_points):
    # get data from querystring if not available directly in the event
    if params is not None:
        querystring = params.get('querystring', None)
    if querystring is not None:
        if not vins:
            vins = querystring.get('vins', None)
            if vins is None:
                raise ArcimotoArgumentError('Input validation failed: vins is a required argument')
            elif not len(vins):
                raise ArcimotoArgumentError('Input validation failed: vins cannot be empty')
            else:
                vins = query_string_parameter_parse_values(vins)
        if not telemetry_points:
            telemetry_points = querystring.get('telemetry_points', None)
            if telemetry_points is None:
                raise ArcimotoArgumentError('Input validation failed: telemetry_points is a required argument')
            elif not len(telemetry_points):
                raise ArcimotoArgumentError('Input validation failed: telemetry_points cannot be empty')
            else:
                telemetry_points = query_string_parameter_parse_values(telemetry_points)
    return (vins, telemetry_points)


def telemetry_point_parse_period(telemetry_point_period):
    # has period with start and end (format: [start:end])
    # split period into start and end
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

    return period


def telemetry_point_parse_input(telemetry_point):
    if '[' in telemetry_point:
        if ']' not in telemetry_point:
            raise ArcimotoArgumentError(f'Input validation failed: malformed telemetry point {telemetry_point} period')
        telemetry_point_pieces = telemetry_point.split('[', 1)
        telemetry_point_name = escape_literal(telemetry_point_pieces[0])
        telemetry_point_period = telemetry_point_pieces[1][:-1]
        # if has [] but not : then is counted as latest request
        if ':' not in telemetry_point_period:
            telemetry_point_period = None
    else:
        telemetry_point_name = escape_literal(telemetry_point)
        telemetry_point_period = None

    return (telemetry_point_name, telemetry_point_period)


def influx_connect_and_prepare_client():
    global InfluxDBClient, TELEMETRY_DB_NAME

    client = InfluxDBClient(host=influx_ip_get(), port=90)
    client.switch_database(TELEMETRY_DB_NAME)

    return client


def influx_ip_get():
    influx_ip = arcimoto.runtime.get_secret(f'telemetry.influxdb.ip.{arcimoto.runtime.get_env()}').get('ip', None)
    if influx_ip is None:
        raise ArcimotoException('Unable to get Influx IP')
    return influx_ip


def validate_user_has_vins_access(user, requested_vins):
    current_username = user.username
    for vin in requested_vins:
        if not arcimoto.vehicle.Vehicle(vin).validate_user_access(current_username):
            raise ArcimotoPermissionError(f'Unauthorized: user {current_username} does not control VIN {vin}.')


def query_string_parameter_parse_values(query_string_parameter):
    return [value.strip() for value in query_string_parameter.split(',')]


def telemetry_point_get_latest(client, vin, telemetry_point):
    # query influxdb for a telemetry point and the corresponding time entry
    # handle gps_position separately
    query_end = (
        'FROM telemetry '
        'GROUP BY * '
        'ORDER BY time '
        'DESC LIMIT 1'
    )
    if telemetry_point == 'gps_position':
        query = 'SELECT gps_latitude, gps_longitude, gps_altitude, time ' + query_end
        results = client.query(query)

        latest = {
            'latitude': None,
            'longitude': None,
            'altitude': None,
            'time': None
        }
        points = results.get_points(tags={'vin': vin})

        for point in points:
            latest['latitude'] = point.get('gps_latitude', None)
            latest['longitude'] = point.get('gps_longitude', None)
            latest['altitude'] = point.get('gps_altitude', None)
            latest['time'] = point.get('time', None)
    elif telemetry_point == 'odometer':
        query = 'SELECT odometer, time ' + query_end
        results = client.query(query.format(escape_literal(telemetry_point)))

        latest = {
            'point': None,
            'time': None
        }
        points = results.get_points(tags={'vin': vin})
        for point in points:
            latest['point'] = point.get('odometer', None)
            latest['time'] = point.get('time', None)

        if latest.get('point', None) is None:
            query = (
                'SELECT last_odometer, time '
                'FROM "365d"."telemetry" '
                'GROUP BY * '
                'ORDER BY time '
                'DESC LIMIT 1'
            )
            results = client.query(query.format(escape_literal(telemetry_point)))

            latest = {
                'point': None,
                'time': None
            }
            points = results.get_points(tags={'vin': vin})
            for point in points:
                latest['point'] = point.get('last_odometer', None)
                latest['time'] = point.get('time', None)
    else:
        query = 'SELECT {}, time ' + query_end
        results = client.query(query.format(escape_literal(telemetry_point)))

        latest = {
            'point': None,
            'time': None
        }
        points = results.get_points(tags={'vin': vin})
        for point in points:
            latest['point'] = point.get(telemetry_point, None)
            latest['time'] = point.get('time', None)

    return latest


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

    results = client.query(
        query=query,
        bind_params={
            'vin': vin
        }
    )

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


lambda_handler = vehicles_telemetry_get
