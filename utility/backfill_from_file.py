#!/usr/bin/env python3
"""
    Name:
        backfill_from_file.py
    Category:
        This file is part of AWSLambda.
    Purpose:
        Read telemetry data from a text file and ingest it into InfluxDB.
        The text files must be present on the InfluxDB server.
"""
import boto3
import json
import csv
import os
import logging

from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from dateutil.parser import parse
from datetime import datetime

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

DBNAME = 'amtelemetry'
MY_REGION = 'us-west-2'


def reset_db(env=None, client=None, longRP=False):
    """
    Purpose:
        Reset the InfluxDB to have the db DBNAME with 30d and 365d RPs and all telemetry-point based CQs
    Note:
        This function will not work in the prod environment.  Is is for dev and staging only.
    Inputs:
        env: the environment (dev, staging, or prod)
        client: the influxDB client.  If not provided, one will be created.
        longRP: set to True to switch default RP to 365d (but keep '30d' name)
    Returns:
        If erroneously run in prod: raises Exception
        Otherwise: returns response from Lambda function set_continuous_queries
    """
    # do not run this function in prod environment
    if env is None:
        logger.error("Error: env must be specified.  Function exiting.")
        raise Exception("env is required to run reset_db")
    elif env == "prod":
        logger.error("Error: function reset_db must not be run in prod environment.  Function exiting.")
        raise Exception("Do not run reset_db in prod environment.")
    else:  # run in dev or staging
        # get InfluxDB client
        if client is None:
            client = get_default_client()

        # drop amtelemtry and recreate it with RPs
        client.drop_database(DBNAME)
        client.create_database(DBNAME)
        if longRP:
            client.create_retention_policy('30d', '30d', 1, default=False)
            client.create_retention_policy('365d', '365d', 1, default=True)
        else:
            client.create_retention_policy('30d', '30d', 1, default=True)
            client.create_retention_policy('365d', '365d', 1, default=False)

        # use lambda to create CQs
        aws_lambda = boto3.client('lambda', MY_REGION)
        try:
            response = aws_lambda.invoke(FunctionName=f"arn:aws:lambda:us-west-2:511596272857:function:set_continuous_queries:{env}")
        except Exception as e:
            logger.error(f"Error encounterd in function set_continous_queries: {e}")
        else:
            return response


def handle_field(name, field, jdata, time_key="timestamp"):
    """ This function copied from telemetry_vpc_ingest_influx.py; modified for timestamp, vin, group, name removal """
    if name == 'gps_position':
        try:
            lat_lon = field.split(",")
            jdata['gps_latitude'] = float(lat_lon[0])
            jdata['gps_longitude'] = float(lat_lon[1])
        except AttributeError as e:
            logger.info(f"GPS position: {field}")
            logger.info(f"GPS position split error: {e}")
        return
    elif name == 'gps_altitude' and field is None:
        return
    elif name == time_key:
        # dateobj = parse(field)
        # jdata['timestamp'] = int(round(dateobj.timestamp() * 1000))
        return
    elif name == "vin":
        return
    elif name == "group":
        return
    elif name == "name":
        return
    elif name == "host":
        return
    elif isinstance(field, bool):
        # Convert all boolean values to floats or integers because otherwise Telegraf will convert them to strings and throw them out
        if name == 'vehicle_started':  # specific exceptions here
            field = int(field)
        else:
            field = float(field)
    elif isinstance(field, int):
        # Convert other ints to floats
        field = float(field)
    # remove empty string fields; kludge others to floats
    elif isinstance(field, str):
        if field == "":
            return
        else:
            field = float(field)
    # default is pass through
    jdata[name] = field
    return


def send_telemetry_quantum(vin, quantum, client, modify2000=False, retention_policy="30d", env_prefix="", time_key="timestamp", time_unit="s"):
    """
    vin: the VIN of the vehicle
    quantum: a json telemetry object
    client: the InfluxDBClient
    modify2000: set to True to change overwrite comm module default "2000-00-00" timestamps with "2000-01-01"
        However, if this is older than the influxdb retention policy, the timestamps will not enter the db.
    retention_policy: the RP to insert data into in the DB
    env_prefix: prefix, including dash for VIN for insert into DB
        Should be "", "STAGE-", or "DEV-"
        Default: ""
    time_key: the name of the time key in the quantum
    time_unit: the unit of time.  Should be "s" or "ns" only.
    """
    if "60.00Z" in quantum[time_key]:
        logger.info(f"Bogus time stamp detected: {quantum[time_key]}.  Data point thrown out.")
        return
    if modify2000:
        quantum[time_key] = quantum[time_key].replace('2000-00-00', '2000-01-01')

    telemetry_dict = {}
    fields = {}
    dateobj = parse(quantum[time_key])
    if time_unit == "s":
        telemetry_dict["time"] = int(round(dateobj.timestamp() * 10**9))  # POSIX time * 10^9
    elif time_unit == "ns":
        telemetry_dict["time"] = int(round(dateobj.timestamp()))
    else:
        raise Exception("Invalid time unit!")
    telemetry_dict["measurement"] = "telemetry"
    telemetry_dict["tags"] = {"vin": env_prefix + vin}
    for record in quantum:
        handle_field(record, quantum[record], fields, time_key=time_key)
    if fields == {}:
        return  # no data to send
    telemetry_dict["fields"] = fields
    # logger.info("telemetry_dict: {}".format(json.dumps(telemetry_dict)))
    try:
        client.write_points([telemetry_dict], retention_policy=retention_policy, time_precision='n')
    except InfluxDBClientError as e:
        logger.error(f"Write error! {e}: Could not write fields: {telemetry_dict}")
        raise e


def get_default_client():
    host = 'localhost'
    port = 8086
    user = 'root'
    password = 'root'
    return InfluxDBClient(host, port, user, password, DBNAME)


def send_telemetry_batch(vin, telemetry_file, modify2000=False, env="", client=None):
    """
    vin: the VIN of the vehicle
    telemetry_file: the name of the file which contains a series of json telemetry quanta
    modify2000: set to True to change overwrite comm module
        default "2000-00-00" timestamps with "2000-01-01"
        However, if this is older than the influxdb retention policy, the timestamps will not enter the db.
    env: prefix (including dash) to VIN for insert into DB
        Should be "", "STAGE-", or "DEV-"
        Default: ""
    client: the InfluxDBClient.  If not provided, one will be created.
    """
    # get InfluxDB client
    if client is None:
        client = get_default_client()

    # create 30 year RP
    if modify2000:
        client.create_retention_policy('30year', '10957d', 1, default=False)
        retention_policy = '30year'
    else:
        retention_policy = '30d'

    count_lines = 0
    with open(telemetry_file, 'r') as input_file:
        for line in input_file:
            # logger.info(line[:-1])
            quantum = json.loads(line[:-1])  # remove \n
            send_telemetry_quantum(vin, quantum, client, modify2000, retention_policy, env)
            count_lines += 1
    logger.info(f'number of lines: {count_lines}')


def replace_date_in_timestamp(posix_timestamp, ISO_date):
    """
    changes posix timestamp to represent the same time of day but the day specified by ISO_date
        Note: change is not done in-place to input.  Rather:
    returns a posix timestamp
    """
    ISO_timestamp = datetime.fromtimestamp(int(posix_timestamp) / 10**9).isoformat()
    new_timestamp = ISO_timestamp.replace(ISO_timestamp[:10], ISO_date)
    dateobj = parse(new_timestamp)
    return int(round(dateobj.timestamp() * 10**9))


def send_telemetry_csv(telemetry_file, env_prefix="", client=None, replace_date=False, replace_vin=False):
    """
    telemetry_file: the name of the csv file which contains telemtery data for one vehicle
        Must include all DB keys: name, time, group, host, vin
    env_prefix: prefix (including dash) to VIN for insert into DB
        Should be "", "STAGE-", or "DEV-"
        Default: ""
    client: the InfluxDBClient.  If not provided, one will be created.
    replace_date: set to ISO date to replace date in sent quantum, or False to do no replacement
    replace_vin: set to VIN to replace VIN in sent quantum, or False to do no replacement
    """
    # get InfluxDB client
    if client is None:
        client = get_default_client()

    with open(telemetry_file, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            time_unit = "ns"
            # logger.info(f"row: {row}")
            if replace_date:
                row["time"] = replace_date_in_timestamp(row["time"], replace_date)
            if isinstance(row["time"], int):
                row["time"] = datetime.fromtimestamp(row["time"] / 10**9).isoformat()
                time_unit = "s"
            if replace_vin:
                vin = str(replace_vin)
            else:
                vin = str(row["vin"])
            # logger.info(f"vin: {vin}")
            send_telemetry_quantum(vin, row, client, env_prefix=env_prefix, time_key="time", time_unit=time_unit)


###############################################################################
# testing

if __name__ == '__main__':
    # pick a VIN and directory
    vin = '7F7ATR315KER00010'  # "the Marketing Vehicle"
    file_dir = "KER00010"

    # get files
    file_list = os.listdir(file_dir)

    # send data
    for file in file_list:
        bff.send_telemetry_batch(vin, os.path.join(file_dir, file))
        logger.info(f"done with file {file}")
