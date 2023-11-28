#!/bin/bash

# Name: influx_csv_backup.sh
# Purpose: Back up one day of telemetry from EC2 to S3
# Usage: Script is executed via sudo crontab -e
# Inputs:
#   $1 argument is the environment dev, staging, or prod
#   $2 argument is a number of days to offset the reporting from the standard -16
# Location:
#   Script located in influxdb ec2 instance under /opt/config/influx_csv_backup.sh
# Procedure:
#   The script dumps vin_list.csv from local influxdb, iterates each vin,
#   dumps vin data to a yyyy--mm-dd.csv file and then pushes it to arcimoto-telemetry-backup/intake/vin folder
#   finally the script deletes the temporary csv file
#   log output is dumped to /var/log/influx_csv_backup/$1/yyyy-mm-dd.log

day_offset=0
if [[ -z $2 ]]; then
  day_offset=0
else
  day_offset=$2
fi
let start_offset=1+$day_offset
let end_offset=0+$day_offset

TODAY=`date +%Y-%m-%d`
START_RUNTIME=`date +%s`
# Set start and end dates
START=`date +%Y-%m-%d -d "$start_offset day ago"`
END=`date +%Y-%m-%d -d "$end_offset day ago"`

# Set a sleep per vehicle to reduce stress on server
WAIT_TIME=1

# Set path and file name
LOCAL_PATH="opt/config"
# LOG_PATH=${LOCAL_PATH}/logs
LOG_PATH="/var/log/influx_csv_backup/"$1
LOG_FILE_NAME=${TODAY}.log
CSV_FILENAME="${START}.csv"

# Setup simple log dump
exec >> /${LOG_PATH}/${LOG_FILE_NAME} 2>&1

echo "Run Date: "$TODAY
echo "Data Start Date: "$START
echo "Data End Date: "$END

# get VIN list from local influx
VIN_LIST_FILE_NAME="vin_list.csv"
influx -database 'amtelemetry' -host 'localhost' -port 90 -execute 'show tag values with key=vin' -format 'csv' > /${LOCAL_PATH}/${VIN_LIST_FILE_NAME}

# Iterate vin list
BACKUP_BUCKET="arcimoto-telemetry-backup"
BACKUP_PATH="intake/$1"
tail -n +2 /${LOCAL_PATH}/${VIN_LIST_FILE_NAME} | while read i; do # influx CSV VIN list, tail -n +2 cuts the header line
    # Trim 'telemetry,vin' from each line
    VIN=$(echo $i | sed -n -e 's/telemetry\,vin\,//p')
    # Export csv from influx of date range for vin
    influx -database 'amtelemetry' -host 'localhost' -port 90 -execute 'SELECT * FROM "telemetry" WHERE time > '\'${START}\'' and time < '\'${END}\'' AND "vin"='\'''$VIN''\''' -format 'csv' > /${LOCAL_PATH}/${CSV_FILENAME}
    LENGTH=`wc -l < /${LOCAL_PATH}/${CSV_FILENAME}`
    if (($LENGTH > 1)); then
        echo vin: ${VIN} found data, uploading
        aws s3 cp /${LOCAL_PATH}/${CSV_FILENAME} s3://${BACKUP_BUCKET}/${BACKUP_PATH}/${VIN}/ --only-show-errors
    else
        echo vin: ${VIN} no data for date range, skipping
    fi
    sleep $WAIT_TIME
done

END_RUNTIME=`date +%s`
RUNTIME=$((END_RUNTIME-START_RUNTIME))

# remove the local csv file
rm /${LOCAL_PATH}/${CSV_FILENAME}

echo ran in $RUNTIME seconds
