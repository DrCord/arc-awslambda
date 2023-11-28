#!/usr/bin/env python3
"""
    Name:
        influx_backfill.py
    Category:
        This file is part of AWSLambda.
    Purpose:
        Read telemetry data from a text file and send it to a Lambda function for ingestion into InfluxDB.
    Note:
        This method is very slow for loading data into InfluxDB.  For a faster method, use backfill_from_file.py
"""
import json
import boto3
import logging
import os
import argparse

client = boto3.client('lambda')

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def env_from_vin(vin):
    """
    Purpose: get the environment from vin
    """
    if vin[:4] == 'DEV-':
        return 'dev'
    elif vin[:6] == 'STAGE-':
        return 'staging'
    else:
        return 'prod'


def send_telemetry_quantum(vin, quantum, modify2000=False):
    """
    vin: the vin of the vehicle
    quantum: a json telemetry object
    modify2000: set to True to change overwrite comm module default "2000-00-00" timestamps with "2000-01-01"
        However, if this is older than the influxdb retention policy, the data will not actually enter the db.
    """
    if modify2000:
        quantum['timestamp'] = quantum['timestamp'].replace('2000-00-00', '2000-01-01')
    telemetry_dict = {}
    telemetry_dict["vin"] = vin
    telemetry_dict["data"] = [quantum]
    logger.info("Sending {}...".format(telemetry_dict))

    qualifier = env_from_vin(vin)

    try:
        response = client.invoke(
            FunctionName='telemetry_vpc_ingest_influx',
            InvocationType='RequestResponse',  # 'DryRun'?
            # InvocationType='DryRun',
            LogType='Tail',
            # ClientContext='influx_backfill.py',
            Payload=json.dumps(telemetry_dict),
            Qualifier=qualifier
        )
    except Exception as e:
        logger.error(f"Error sending telemetry quantum {quantum}: {e}")
        raise e
    else:
        return response


def send_telemetry_batch(vin, telemetry_file, modify2000=False):
    count_lines = 0
    with open(telemetry_file, 'r') as input_file:
        for line in input_file:
            # logger.info(line[:-1])
            quantum = json.loads(line[:-1])  # remove \n
            send_telemetry_quantum(vin, quantum, modify2000)
            count_lines += 1
    logger.info('number of lines: {}'.format(count_lines))
    logger.info('env: {}'.format(env_from_vin(vin)))


###############################################################################
# testing

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='Take high-resolution vehicle telemetry data backfill into Influx')
    parser.add_argument('vin', help='VIN to be associated with data to be backfilled')
    parser.add_argument('source', help='path to file or flat directory with data to be backfilled')
    args = parser.parse_args()
    vin = args.vin
    tel_path = args.source
    
    if tel_path is not None:
        if os.path.isdir(tel_path):
            os.chdir(tel_path)
            for file in os.listdir(tel_path):
                if os.path.isfile(file):
                    send_telemetry_batch(vin, file)
                elif os.path.isdir(file):
                    print("{} is a directory. Skipping...".format(file))
        elif os.path.isfile(tel_path):
            send_telemetry_batch(vin, tel_path)
        else:
            print("No valid path provided!")
