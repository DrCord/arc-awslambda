import logging
import time
import datetime
import boto3
from botocore.exceptions import ClientError

from arcimoto.exceptions import *
import arcimoto.runtime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

BUCKET = 'arcimoto-telemetry-backup'

cw_logs_client = boto3.client('logs')
s3_client = boto3.client('s3')

@arcimoto.runtime.handler
def monitor_influxdb_backup():
    env = arcimoto.runtime.get_env()
    # get dates
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    last_backup = today - datetime.timedelta(days=1)  # value of "days" must match the offset+1 in the backup script on the EC2
    # get iso format dates
    today_date = today.isoformat()
    tomorrow_date = tomorrow.isoformat()
    backup_date = last_backup.isoformat()
    # get posix format dates
    start_date_posix = int(time.mktime(today.timetuple()))
    end_date_posix = int(time.mktime(tomorrow.timetuple()))

    # or take it back 1 day
    # yesterday = today - datetime.timedelta(days=1)
    # end_date_posix = int(time.mktime(today.timetuple()))
    # start_date_posix = int(time.mktime(yesterday.timetuple()))

    # check for the existence of the log file
    logGroups = {"dev": "DEV-influx-csv-backup",
                 "staging": "STAGE-influx_csv_backup",
                 "prod": "influx_csv_backup"
                }
    logStreams ={"dev": "i-0aea13793a77d647d",
                 "staging": "i-046d48b26d0fd82ca",
                 "prod": "i-003cc9f4047edc985"
                } 
    try:
        response = cw_logs_client.get_log_events(
            logGroupName=logGroups[env],
            logStreamName=logStreams[env],
            startTime=start_date_posix * 1000,
            endTime=end_date_posix * 1000
        )
    except Exception as e:
        logger.debug(f"Error: There was a problem retrieving the InfluxDB backup log file for {today_date}.")
        raise ArcimotoAlertException(f"Error: There was a problem retrieving the InfluxDB backup log file for {today_date}: {e}.")

    # logger.debug("get_log_events response: {}".format(response))
    logger.debug("using response['events']")
    groups = response['events']
    for group in groups:
        message_split = group['message'].split()
        if "vin:" == message_split[0]:
            # logger.debug("timestamp: {}, message: {}".format(group['timestamp'], group['message']))
            vin = message_split[1]
            action = message_split[-1]
            logger.debug(f"vin: {vin}, action: {action}")

            if action == "uploading":
                # check s3 to see that the file is there
                # This S3 key must match those defined in the backup script
                key = f'intake/{env}/{vin}/{backup_date}.csv'
                try:
                    obj = s3_client.head_object(Bucket=BUCKET, Key=key)
                except ClientError as e:
                    if e.response['Error']['Code'] == "404":
                        # The object does not exist.
                        logger.debug(f"Error: The InfluxDB backup file {key} does not exist in S3: {e}")
                        raise ArcimotoAlertException(f"Error: The InfluxDB backup file {key} does not exist in S3: {e}")
                    else:
                        logger.debug(f"Error: There was a problem checking for file {key} on S3: {e}")
                        raise ArcimotoAlertException(f"Error: There was a problem checking for file {key} on S3: {e}")
                else:
                    # The object does exist.
                    logger.debug(f"Backup file {key} is on S3.")
    return {}


lambda_handler = monitor_influxdb_backup
