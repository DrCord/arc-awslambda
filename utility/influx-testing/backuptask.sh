#!/bin/bash
VIN=$1

START=`date +%Y-%m-%d -d "1 day ago"`
END=`date +%Y-%m-%d`

echo $VIN
echo "Start: "$START
echo "End: "$END

#START="2019-03-18"
#END="2019-03-19"

influx -database 'amtelemetry' -host 'localhost' -execute 'SELECT * FROM "amtelemetry".""."tel_test" WHERE time > '\'${START}\'' and time < '\'${END}\'' AND "vin"='\'''$VIN''\''' -format 'csv' > /opt/exports/${START}.csv
aws s3 cp /opt/exports/${START}.csv s3://arcimoto-telemetry/intake/${VIN}/
