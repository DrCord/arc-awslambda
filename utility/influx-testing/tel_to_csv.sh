#!/usr/bin/env bash
#
# Name:
#       tel_to_csv.sh
# Category:
#       This file is part of AWSTelemetry.
# Purpose:
#       Extract some information from influxdb and export it to csv
# Requirements:
#       Run this on the influxdb server.  Need influx available to execute.
# Inputs:
#       $1: the date for which to extract telemetry data
#       $2: the VIN for the vehicle for which to extract data (optional)
# Example usage:
#       $ ./tel_to_csv.sh 2019-10-01 7F7ATR316KER00002
#
# Written by Z Knight, 2019.10.02
#       Specified -precision rfc3339; ZK, 2019.10.03
#       Added -port 90 to make influx work after reboot; ZK, 2019.10.17

function extract_telemetry {
  local  __resultvar=$1
  if [ -z "$2" ]
    then
      echo "No date specified. Will use yesterday."
      start_date=$(date +%Y-%m-%d -d "-1 day")
    else
      start_date=$2
  fi
  end_date=$(date +%Y-%m-%d -d "$start_date +1 day") || exit
  if [ -z "$3" ]
    then
      vin_string=""
      save_file=$start_date$"_allVINs"".csv"
    else
      vin_string="and vin='$3'"
      save_file=$start_date$"_"$3".csv"
  fi

  execute_string="SELECT * FROM \"telemetry\" WHERE time > '"$start_date"' and time < '"$end_date"' "$vin_string
  influx -database "amtelemetry" -port 90 -execute "$execute_string" -precision rfc3339 -format 'csv' > $save_file || exit

  local  my_result=$save_file
  eval $__resultvar="'$my_result'"
}

extract_telemetry result $1 $2
echo "file "$result" created."
