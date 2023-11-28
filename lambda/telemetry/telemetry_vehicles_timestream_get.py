import logging
# import json
# from datetime import datetime, timedelta
import boto3
from botocore.config import Config
from collections import defaultdict
import copy

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

REGION = 'us-west-2'
env = None


@arcimoto.runtime.handler
def telemetry_vehicles_timestream_get(vins, telemetry_points, params):
    global env, logger

    user = arcimoto.user.current()
    if not user.authenticated:
        raise ArcimotoPermissionError('Unauthorized telemetry request by guest')

    # get data from querystring if not available directly in the event
    # only overwrites vins or telemetry points from params if they are None
    if not vins or not telemetry_points:
        (vins, telemetry_points) = query_string_get_parameters(params, vins, telemetry_points)

    validate_vins_exist(vins)
    validate_user_has_vins_access(user, set(vins))

    env = arcimoto.runtime.get_env()

    vehicles_telemetry_points = telemetry_points_get_data_for_vins(telemetry_points, vins)

    return {
        'vehicles_telemetry_points': vehicles_telemetry_points
    }


def create_query_client():
    '''
    ## Create a timestream query client.
    '''
    global REGION
    config = Config()
    session = boto3.Session()
    client = session.client(
        service_name='timestream-query',
        region_name=REGION,
        config=config
    )

    return client


def db_info_get():
    global env
    db_name = 'telemetry'
    if env != 'prod':
        db_name += '-' + env
    db_table = 'vehicles'

    return (db_name, db_table)


def create_query_latest(vin, telemetry_point):
    (db_name, db_table) = db_info_get()
    if telemetry_point in ['gps_latitude', 'gps_longitude']:
        if telemetry_point == 'gps_latitude':
            telemetry_point_db_name = 'lat'
        else:
            telemetry_point_db_name = 'long'
        query = (
            'SELECT measure_name, "measure_value::double", time '
            f'FROM "{db_name}"."{db_table}" '
            f"WHERE vin = '{vin}' "
            f"AND measure_name = '{telemetry_point_db_name}' "
            'ORDER BY vin ASC, time DESC '
            'LIMIT 1'
        )
    else:
        query = (
            'SELECT "measure_value::double", "measure_value::boolean", time '
            f'FROM "{db_name}"."{db_table}" '
            f"WHERE vin = '{vin}' "
            f"AND measure_name = '{escape_literal(telemetry_point)}' "
            'ORDER BY vin ASC, time DESC '
            'LIMIT 1'
        )

    return query


def create_query_period(vin, telemetry_point, period):
    (db_name, db_table) = db_info_get()

    start_safe = escape_literal(period.get('start'))
    end_safe = escape_literal(period.get('end'))

    telemetry_point_safe = escape_literal(telemetry_point)
    
    if telemetry_point == 'gps_position':
        query = (
            'SELECT measure_name, "measure_value::double", time '
            f'FROM "{db_name}"."{db_table}" '
            f"WHERE vin = '{vin}' "
            f"AND (measure_name = 'lat' OR measure_name = 'long') "
        )
    else:
        query = (
            'SELECT "measure_value::double", "measure_value::boolean", time '
            f'FROM "{db_name}"."{db_table}" '
            f"WHERE vin = '{vin}' "
            f"AND measure_name = '{telemetry_point_safe}' "
        )

    if end_safe == 'now':
        if start_safe.endswith('ms'):
            milliseconds = start_safe.replace('ms', '')
            if milliseconds.isnumeric():
                query += (
                    f'AND time between from_milliseconds({milliseconds}) and now() '
                )
            else:
                raise ArcimotoArgumentError('Query failed: cannot use a non numeric milliseconds entry for the start time.')
        else:
            query += (
                f'AND time >= now() - {start_safe} '
            )
    else:
        if start_safe.endswith('ms') or end_safe.endswith('ms'):
            if start_safe.endswith('ms') and end_safe.endswith('ms'):
                start_milliseconds = start_safe.replace('ms', '')
                end_milliseconds = end_safe.replace('ms', '')
                if start_milliseconds.isnumeric() and end_milliseconds.isnumeric():
                    query += (
                        f'AND time between from_milliseconds({start_milliseconds}) and from_milliseconds({end_milliseconds}) '
                    )
                else:
                    raise ArcimotoArgumentError('Query failed: cannot use a non numeric milliseconds entry for the time.')
        else:
            query += (
                f'AND time between ago({start_safe}) and ago({end_safe}) '
            )

    query += (
        'ORDER BY vin ASC, time DESC'
    )

    return query


def execute_query(client, query):
    # Execute the passed query using the specified client.
    try:
        pages = None
        queryId = None
        # Create the paginator to paginate through the results.
        paginator = client.get_paginator('query')
        pageIterator = paginator.paginate(QueryString=query)
        emptyPages = 0
        pages = list()
        lastPage = None
        for page in pageIterator:
            if 'QueryId' in page and queryId is None:
                queryId = page['QueryId']

            lastPage = page

            if 'Rows' not in page or len(page['Rows']) == 0:
                # We got an empty page.
                emptyPages += 1
            else:
                pages.append(page)

        # If there were no result, then return the last empty page to carry over the query results context
        if len(pages) == 0 and lastPage is not None:
            pages.append(lastPage)
        return pages
    except Exception as e:
        if queryId is not None:
            # Try canceling the query if it is still running
            try:
                client.cancel_query(query_id=queryId)
            except Exception as e:
                pass
        raise ArcimotoException('Unable to execute query: {}'.format(e))


# Execute the passed query using the client and return the result as a dataframe.
def execute_query_and_return_as_dataframe(client, query):
    return flat_model_to_dataframe(execute_query(client, query))


def parse_scalar(c_type, data):
    if data is None:
        return None
    if (c_type == "VARCHAR"):
        return data
    elif (c_type == "BIGINT"):
        return int(data)
    elif (c_type == "DOUBLE"):
        return float(data)
    elif (c_type == "INTEGER"):
        return int(data)
    elif (c_type == "BOOLEAN"):
        return bool(data)
    elif (c_type == "TIMESTAMP"):
        return data
    else:
        return data


def parse_array_data(c_type, data):
    if data is None:
        return None
    datum_list = []
    for elem in data:
        datum_list.append(parse_datum(c_type['Type'], elem))
    return datum_list


def parse_ts_data(c_type, data):
    if data is None:
        return None
    datum_list = []
    for elem in data:
        ts_data = {}
        ts_data['time'] = elem['Time']
        ts_data['value'] = parse_datum(c_type['Type'], elem['Value'])
        datum_list.append(ts_data)
    return datum_list


def parse_row_data(c_types, data):
    if data is None:
        return None
    datum_dict = {}
    for c_type, elem in zip(c_types, data['Data']):
        datum_dict[c_type['Name']] = parse_datum(c_type['Type'], elem)
    return datum_dict


def parse_datum(c_type, data):
    if ('ScalarType' in c_type):
        return parse_scalar(c_type['ScalarType'], data.get('ScalarValue'))
    elif ('ArrayColumnInfo' in c_type):
        return parse_array_data(c_type['ArrayColumnInfo'], data.get('ArrayValue'))
    elif ('TimeSeriesMeasureValueColumnInfo' in c_type):
        return parse_ts_data(c_type['TimeSeriesMeasureValueColumnInfo'], data.get('TimeSeriesValue'))
    elif ('RowColumnInfo' in c_type):
        return parse_row_data(c_type['RowColumnInfo'], data.get('RowValue'))
    else:
        raise Exception("All the data is Null???")


def flat_model_to_dataframe(items):
    """
    Translate a Timestream query SDK result into ideal structure.
    """
    return_val = defaultdict(list)
    for obj in items:
        for row in obj.get('Rows'):
            for c_info, data in zip(obj['ColumnInfo'], row['Data']):
                c_name = c_info['Name']
                c_type = c_info['Type']
                return_val[c_name].append(parse_datum(c_type, data))

    return return_val


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


def query_string_parameter_parse_values(query_string_parameter):
    return [value.strip() for value in query_string_parameter.split(',')]


def telemetry_points_get_data_for_vins(telemetry_points, vins):
    vehicles_telemetry_points = {}

    client = create_query_client()

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


def telemetry_point_parse_period(telemetry_point_period):
    # has period with start and end (format: [start:end])
    # split period into start and end
    telemetry_point_periods = telemetry_point_period.split(':')
    period_start = telemetry_point_periods[0]
    if telemetry_point_periods[1] == '':
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


def validate_user_has_vins_access(user, requested_vins):
    current_username = user.username
    for vin in requested_vins:
        if not arcimoto.vehicle.Vehicle(vin).validate_user_access(current_username):
            raise ArcimotoPermissionError(f'Unauthorized: user {current_username} does not control VIN {vin}.')


def telemetry_point_get_latest(client, vin, telemetry_point):
    # query timestream for a telemetry point and the corresponding time entry
    # handle gps_position separately
    if telemetry_point == 'gps_position':
        latest = {
            'latitude': None,
            'longitude': None,
            'time': None
        }
        gps_position_points = [
            'gps_latitude',
            'gps_longitude'
        ]
        for gps_position_point_name in gps_position_points:
            query = create_query_latest(vin, gps_position_point_name)
            results = execute_query_and_return_as_dataframe(client, query)

            measure_times = results.get('time', [])
            measure_values = results.get('measure_value::double', [None])

            if latest['time'] is None or latest['time'] == measure_times[0]:
                if len(measure_times) and measure_values[0] is not None:
                    latest['time'] = measure_times[0]
                    if 'latitude' in gps_position_point_name:
                        latest['latitude'] = measure_values[0]
                    else:
                        latest['longitude'] = measure_values[0]
            else:
                raise ArcimotoException(f'gps data points times do not match. gps position: {latest}, {vin}/{gps_position_point_name} query results: {results}')

    else:
        latest = {
            'point': None,
            'time': None
        }
        query = create_query_latest(vin, telemetry_point)
        results = execute_query_and_return_as_dataframe(client, query)

        measure_times = results.get('time', [])
        measure_values = results.get('measure_value::double', [None])
        if measure_values[0] is None:
            measure_values = results.get('measure_value::boolean', [None])

        if len(measure_times) and measure_values[0] is not None:
            latest['point'] = measure_values[0]
            latest['time'] = measure_times[0]

    return latest


def telemetry_point_get_period(client, vin, telemetry_point, period):
    # query timestream for a telemetry point for the period
    telemetry_data = []

    if telemetry_point == 'gps_position':
        query = create_query_period(vin, 'gps_position', period)
        results = execute_query_and_return_as_dataframe(client, query)

        measure_names = results.get('measure_name', [None])
        measure_times = results.get('time', [])
        measure_values = results.get('measure_value::double', [None])

        point = {
            'latitude': None,
            'longitude': None,
            'time': None
        }
        count = 0
        for measure_name in measure_names:
            if measure_name is None:
                continue
            if point['time'] is None or point['time'] == measure_times[count]:
                point['time'] = measure_times[count]
                if measure_name == 'lat':
                    point['latitude'] = measure_values[count]
                elif measure_name == 'long':
                    point['longitude'] = measure_values[count]
            else:
                raise ArcimotoException(f'gps data points times do not match. gps position: {point}, {vin}/gps_position query results: {results}')
            if point['time'] is not None and point['latitude'] is not None and point['longitude'] is not None:
                telemetry_data.append(copy.deepcopy(point))
                point = {
                    'latitude': None,
                    'longitude': None,
                    'time': None
                }
    else:
        query = create_query_period(vin, telemetry_point, period)
        results = execute_query_and_return_as_dataframe(client, query)

        measure_times = results.get('time', [])
        measure_values = results.get('measure_value::double', [None])
        count = 0
        for measure_time in measure_times:
            if measure_values[count] is None:
                measure_values = results.get('measure_value::boolean', [None])
            telemetry_data.append({
                'point': measure_values[count],
                'time': measure_time
            })
            count += 1

    return telemetry_data


def escape_literal(literal):
    # since influxdb bind_params only works on the where clause we need to do some sql injection protection
    escaped_literal = literal
    # from https://stackoverflow.com/a/23190083/1291935
    # If there's a zero byte (\x00) in the string, truncate the string before the zero byte
    zero_byte_location = escaped_literal.find('\x00')
    if zero_byte_location != -1:
        escaped_literal = escaped_literal[:zero_byte_location - 1]
    # For every ' in the string, replace it with ''
    escaped_literal = escaped_literal.replace("'", "''")

    return escaped_literal


lambda_handler = telemetry_vehicles_timestream_get
