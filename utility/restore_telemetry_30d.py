#!/usr/bin/env python3
"""
    Name:
        restore_telemetry_30d.py
    Category:
        This file is part of AWSLambda.
    Purpose: retrieve the last 30 days of telemetry .csv files from S3 and insert them into influxDB
        Script will also optionally prepend VINs with a prefix upon insertion into DB
        Default: load "prod" data and reload into influxDB with prefix "STAGE-"
        Optionally: Can load fake "jackknife" data for a random set of fake vehicles.
        Optionally: Can use local files rather than source S3.
"""
import boto3
import logging
import os
import json
import datetime
import random

import backfill_from_file as bff

from botocore.exceptions import ClientError

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

BUCKET = "arcimoto-telemetry-backup"
TEMP_FILE = "telemetry.csv"
VIN_LIST_FILE_NAME = "vin_list.json"
NUM_DAYS = 30
FAKE_VIN_MAX = 1000


def restore_telemetry_30d(logfile_name="restore_telemetry_30d.log", env="prod", env_prefix="", num_faux=10, data_dir=None):
    """
    Name: restore_telemetry_30d
    Purpose: retrieve the last 30 days of telemetry .csv files from S3 and insert them into influxDB
    Inputs:
        logfile_name: the name of the log file to create when restoring data
        env: the environment to restore data from
            If env is "jackknife" then fake data will be used
            Default: "prod"
        env_prefix: the (optional) prefix to prepend VINs with when inserting data into DB
            Default: ""
        num_faux: If env is "jackknife" then this is the number of fake vehicles to randomly use
            Default: 10
        data_dir: The source for local .csv files.  If none, then S3 will be used.
    Outputs:
        saves a vin list file and a log file.
    """
    # set up logging to file
    logging.basicConfig(level=logging.INFO,  # DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M:%S',
                        filename=logfile_name,
                        filemode='w')
    logger_rt3 = logging.getLogger("restore_telemetry_30d")
    logger_rt3.info("Starting data restoration process.")

    # get s3 and infludcb clients
    s3 = boto3.client('s3')
    influxdb = bff.get_default_client()

    if env == "jackknife":
        # create list of fake vins
        # vin_list = [str(random.randrange(1, FAKE_VIN_MAX + 1)) for i in range(num_faux)]
        vin_list = [i + 1 for i in range(num_faux)]
    else:
        # get vin list from s3
        try:
            # get json file
            key = f"config/{env}/{VIN_LIST_FILE_NAME}"
            s3.download_file(BUCKET, key, VIN_LIST_FILE_NAME)
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                # The object does not exist.
                logger_rt3.error(f"Error: The VIN list file {key} does not exist in S3: {e}")
            else:
                logger_rt3.error(f"Error: There was a problem checking for file {key} on S3: {e}")
            raise e
        else:
            # The object does exist.
            logger_rt3.info(f"VIN list file {key} downloaded from S3.")
            with open(VIN_LIST_FILE_NAME) as json_file:
                vin_list = json.load(json_file)

    num_vins = len(vin_list)

    # get day list
    day_list = []
    today = datetime.date.today()
    for day_num in range(NUM_DAYS):
        date_to_add = today - datetime.timedelta(days=day_num)
        iso_date = date_to_add.isoformat()
        day_list.append(iso_date)

    if data_dir:
        file_list = os.listdir(data_dir)
        num_files = len(file_list)

    # loop over telemetry files
    for vin_index, vin in enumerate(vin_list):
        logger.info(f"Starting VIN {vin_index+1}/{num_vins}...")
        for day in day_list:
            key = f"intake/{env}/{vin}/{day}.csv"
            try:
                # get csv file
                if data_dir:
                    random_file_number = random.randint(0, num_files - 1)
                    load_file = os.path.join(data_dir, file_list[random_file_number])
                else:
                    s3.download_file(BUCKET, key, TEMP_FILE)
                    load_file = TEMP_FILE
            except ClientError as e:
                if e.response['Error']['Code'] == "404":
                    # The object does not exist.
                    logger_rt3.error(f"Error: The InfluxDB backup file {key} does not exist in S3: {e}")
                else:
                    logger_rt3.error(f"Error: There was a problem checking for file {key} on S3: {e}")
            else:
                # The object does exist.
                if not data_dir:
                    logger_rt3.info(f"Backup file {key} downloaded from S3.")

                # send data to influx
                try:
                    bff.send_telemetry_csv(load_file, env_prefix=env_prefix, client=influxdb, replace_date=day, replace_vin=vin)
                except Exception as e:
                    logger_rt3.error(f"Exception occured when restoring from file {key}: {e}")
                else:
                    if data_dir:
                        logger_rt3.info(f"Telemtry from file {load_file} loaded into influx for VIN {vin}, day {day}.")
                    else:
                        logger_rt3.info(f"Telemtry from file {key} re-loaded into influx.")

    # remove file
    os.remove(TEMP_FILE)

    # close db client
    influxdb.close()

    logger_rt3.info("Done restoring from backup.")


###############################################################################
# testing

def restoration_time_test(env="staging", env_prefix="STAGE-", num_faux=10):
    """
    Puspose: Does a test where the amount of time to restore from backup is timed.
    Inputs:
        env: the environment for which to set CQs when resetting DB
        env_prefix: the prefix to add to VINs when restoring telemetry data
        num_faux: the number of backups to restore from "jackknife" env
    Returns:
        a datetime timedelta of the time that it took to do the restoration
    """
    # reset the db
    bff.reset_db(env=env, longRP=True)

    # import the data from s3
    start_time = datetime.datetime.now()
    restore_telemetry_30d(env="jackknife", env_prefix=env_prefix, num_faux=num_faux)
    end_time = datetime.datetime.now()

    return end_time - start_time


def restoration_time_set(env="staging", env_prefix="STAGE-", num_faux=10, num_tests=1, save_file="time_set.txt"):
    """
    Wrapper for restoration_time_test.
    Runs that function num_tests number of times, writes results to file, and returns results
    """
    logger.info(f"Number of vehicles to restore: {num_faux}")
    timedeltas = []
    for test_num in range(num_tests):
        logger.info(f" Starting test {test_num+1} of {num_tests}...")
        result = restoration_time_test(env=env, env_prefix=env_prefix, num_faux=num_faux)
        timedeltas.append(result)

    try:
        with open(save_file, 'w') as filehandle:
            for listitem in timedeltas:
                filehandle.write(f"{listitem}\n")
    except Exception as e:
        logger.error(f"Problem saving file {save_file}: {e}")

    return timedeltas


def restoration_time_set_set(set_sizes, env="staging", env_prefix="STAGE-", num_tests=10):
    """
    Wrapper for restoration_time_set.
    Runs restoration_time_set with various numbers of fake vehicles
    Inputs:
        set_sizes: list of the number of vechicles used in each set
            example: [1,10,100] would indicate running num_tests for each of the set sizes 1, 10, and 100
        env:
        env_prefix:
        num_tests: the number of times to restore data for each set size in set_sizes
    Returns:
        list of lists of timedelta objects containing run times
    """
    timedeltas_list = []
    logger.info(f"Starting restoration test with set sizes {set_sizes}, with {num_tests} runs each.")
    for set_size in set_sizes:
        logger.info(f"Starting test with {set_size} runs...")
        save_file = f"time_set_{set_size}.txt"
        timedeltas = restoration_time_set(env=env, env_prefix=env_prefix, num_faux=set_size, num_tests=num_tests, save_file=save_file)
        timedeltas_list.append(timedeltas)
    logger.info("Done with all tests.")
    return timedeltas_list


###############################################################################
# main function

if __name__ == '__main__':
    restore_telemetry_30d(env="prod", env_prefix="STAGE-")
