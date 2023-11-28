#!/usr/bin/env python3
"""
    Name:
        backup_telemetry_analyzer.py
    Category:
        This file is part of AWSLambda.
    Purpose:
        Search through backup telemetry files and determine which files represent close to a full day's worth of telemetry, to within a specified threshold.
        Generate a list of (vin,day) .csv files which meet the criteria.
"""
import boto3
import logging
import csv
import json
import datetime
import random
import matplotlib.pyplot as plt

from botocore.exceptions import ClientError

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

BUCKET = "arcimoto-telemetry-backup"
TEMP_FILE = "telemetry.csv"
VIN_LIST_FILE_NAME = "vin_list.json"


def get_vin_list(env="prod", s3=None):
    if s3 is None:
        s3 = boto3.client('s3')
    key = f"config/{env}/{VIN_LIST_FILE_NAME}"

    try:
        # get json file
        s3.download_file(BUCKET, key, VIN_LIST_FILE_NAME)
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            # The object does not exist.
            logger.error(f"Error: The VIN list file {key} does not exist in S3: {e}")
        else:
            logger.error(f"Error: There was a problem checking for file {key} on S3: {e}")
        raise e
    else:
        # The object does exist.
        logger.info(f"VIN list file {key} downloaded from S3.")
        with open(VIN_LIST_FILE_NAME) as json_file:
            vin_list = json.load(json_file)

    return vin_list


def get_telemetry_csv(vin, day, env="prod", s3=None):
    if s3 is None:
        s3 = boto3.client('s3')
    key = f"intake/{env}/{vin}/{day}.csv"

    try:
        # get csv file
        s3.download_file(BUCKET, key, TEMP_FILE)
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            # The object does not exist.
            logger.error(f"Error: The InfluxDB backup file {key} does not exist in S3: {e}")
        else:
            logger.error(f"Error: There was a problem checking for file {key} on S3: {e}")
    else:
        # The object does exist.
        logger.info(f"Backup file {key} downloaded from S3.")

        # read csv file
        try:
            with open(telemetry_file, newline='') as csv_file:
                reader = csv.DictReader(csv_file)
        except Exception as e:
            logger.error(f"Exception occured when reading csv file {key}: {e}")
        else:
            logger.info(f"Telemtry from file {key} read and measured.")

    return reader


def get_file_list_for_vin(vin, env="prod", s3=None):
    if s3 is None:
        s3 = boto3.client('s3')
    prefix = f"intake/{env}/{vin}/"

    try:
        response = s3.list_objects_v2(
            Bucket=BUCKET,
            Prefix=prefix
        )
    except Exception as e:
        logger.error(f"Failed to get list for {prefix} from S3: {e}")
        raise e
    file_list = []
    contents = response.get("Contents", None)
    if contents is not None:
        for content in contents:
            file_list.append(content['Key'])

    return file_list


def get_file_size(key, s3=None):
    if s3 is None:
        s3 = boto3.client('s3')

    try:
        response = s3.head_object(
            Bucket=BUCKET,
            Key=key
        )
    except Exception as e:
        logger.error(f"Failed to get file size for {key} from S3: {e}")
        raise e

    return response['ContentLength']


def telemetry_file_bytes(vin_list, env="prod", s3=None):
    """
    Inputs:
        vin_list: a list of vins for which to read every backup .csv file for use in gathering insight about what constitutes an entire day of telemetry
        env: the environment: "prod", "staging", or "dev"
        s3: the s3 client.  If not provided, one will be created.
    Returns:
        A list of file sizes, in bytes
    """
    if s3 is None:
        s3 = boto3.client('s3')
    file_bytes = []
    for vin in vin_list:
        logger.info(f" Getting file list for vin {vin}...")
        file_list = get_file_list_for_vin(vin, env)
        for key in file_list:
            logger.info(f"  Getting size for file {key}...")
            n_bytes = get_file_size(key, s3)
            file_bytes.append(n_bytes)

    return file_bytes


def list_full_day_backups(min_bytes=150000, env="prod", s3=None):
    """
    create a list of backup file keys that are larger than the minimum size
    """
    if s3 is None:
        s3 = boto3.client('s3')
    key_list = []
    vin_list = get_vin_list(s3=s3)
    for vin in vin_list:
        logger.info(f" Getting file list for vin {vin}...")
        file_list = get_file_list_for_vin(vin, env)
        for key in file_list:
            logger.info(f"  Getting size for file {key}...")
            n_bytes = get_file_size(key, s3)
            if n_bytes > min_bytes:
                key_list.append(key)

    return key_list


def create_fake_backup_day(num_vehicles=1000, start_num=1, days_ago=0, key_list_file="key_list.txt", s3=None):
    """
    make one day of fake telemetry data for num_vehicles for 1 day days_ago days ago
    VINs will be numbers, starting at start_num and counting upward to start_num + num_vehicles
    """
    if s3 is None:
        s3 = boto3.client('s3')

    # load key list for source telemetry data
    key_list = [line.rstrip('\n') for line in open(key_list_file)]
    num_keys = len(key_list)

    # get iso date
    today = datetime.date.today()
    date_to_add = today - datetime.timedelta(days=days_ago)
    iso_date = date_to_add.isoformat()

    for fake_vin in range(start_num, start_num + num_vehicles):
        # notify
        if (fake_vin) % 100 == 1:
            logger.info(f" Starting fake VIN {fake_vin} of {num_vehicles+start_num-1}...")

        # pick random key
        key_num = random.randrange(0, num_keys)
        copy_source = {
            'Bucket': BUCKET,
            'Key': key_list[key_num]
        }

        # destination
        dest_key = f"intake/jackknife/{fake_vin}/{iso_date}.csv"

        # copy to fake backup directory
        s3.copy(copy_source, BUCKET, dest_key)

    logger.info(f"backup day {days_ago+1} created.")


def create_fake_backup_month(num_vehicles=1000, start_num=1, key_list_file="key_list.txt", s3=None, num_days=30):
    """
    wrapper for create_fake_backup_day that runs for a month
    """
    if s3 is None:
        s3 = boto3.client('s3')

    for days_ago in range(30):
        logger.info(f"Starting day {days_ago+1} of {num_days}...")
        create_fake_backup_day(num_vehicles=num_vehicles, start_num=start_num, days_ago=days_ago, key_list_file=key_list_file, s3=s3)

    logger.info("Done creating month of fake data.")


###############################################################################
# testing

def test_1(save_file="test_1.txt", n_bins=100):
    """
    Create a histogram of file sizes and save them to a file
    """
    s3 = boto3.client('s3')
    vin_list = get_vin_list(s3=s3)
    file_bytes = telemetry_file_bytes(vin_list, s3=s3)

    with open(save_file, 'w') as filehandle:
        for listitem in file_bytes:
            filehandle.write(f"{listitem}\n")

    plt.hist(file_bytes, bins=n_bins)
    plt.xlabel('bytes')
    plt.ylabel('number of telemetry backup files')
    plt.title('telemtry backup file size distribution')
    plt.show()

    logger.info("the end.")


def test_2(save_file="key_list.txt"):
    """
    Save the list of keys for files larger than the threshold
    """
    key_list = list_full_day_backups()

    with open(save_file, 'w') as filehandle:
        for listitem in key_list:
            filehandle.write(f"{listitem}\n")

    logger.info("the end.")


def test_3(key_list_file="key_list.txt", save_dir="./telemetry/", s3=None):
    """
    Retrieve and save a local copy of all days in key_list
    Note: s3.download_file will not create a directory, so save_dir must exist
    """
    if s3 is None:
        s3 = boto3.client('s3')

    if key_list_file is None:
        key_list = list_full_day_backups()
    else:
        with open(key_list_file, 'r') as f:
            key_list_with_newlines = f.readlines()
        key_list = [key[:-1] for key in key_list_with_newlines]

    for key_num, key in enumerate(key_list):
        logger.info(f"Downloading file {key}...")
        try:
            s3.download_file(BUCKET, key, save_dir + str(key_num) + ".csv")
        except Exception as e:
            logger.error(f"Failed to download file {key}: {e}")

    logger.info("done.")

###############################################################################
# main function


if __name__ == '__main__':
    test_1()
