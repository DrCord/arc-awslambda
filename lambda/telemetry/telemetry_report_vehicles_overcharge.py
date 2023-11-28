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

REGION = 'us-west-2'
env = None


@arcimoto.runtime.handler
def telemetry_report_vehicles_overcharge():
    global env, logger

    env = arcimoto.runtime.get_env()

    client = create_query_client()
    query = create_query_period()
    results = execute_query_and_return_as_dataframe(client, query)

    problem_vins = results.get('vin', [])

    return {
        'problem_vins': problem_vins,
        'problem_count': len(problem_vins)
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


def create_query_period():
    (db_name, db_table) = db_info_get()

    query = (
        'SELECT DISTINCT vin '
        f'FROM "{db_name}"."{db_table}" '
        f"WHERE measure_name = 'bms_pack_soc' "
        'AND "measure_value::double" > 91 '
        f'AND time >= now() - 21d '
        'ORDER BY vin ASC'
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
            except Exception:
                pass
        raise ArcimotoException('Unable to execute query: {}'.format(e)) from e


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


lambda_handler = telemetry_report_vehicles_overcharge
