# AWSTelemetry/utility/Influx Testing
Various utilities for testing influx

## nginx
nginx configuration files for InfluxDB server

## backuptask.sh
Exports a csv of today - 1 through today and uploads it to S3. One file = 8.6MB. 258MB / month. 3,096MB / year.
bash test_backup.sh JRN7FM

## [commands.md](commands.md)
Sample influx commands for managing databases

## generate_vins.py
Creates random VINs

## [influx_prod_to_staging.md](influx_prod_to_staging.md)
A procedure for copying the production telemetry database to the staging server

## tel_to_csv.sh
Export data from influx to a csv file, one day at a time.  Runs on the influxdb server.

Example usage (on the influx server):
```
$ ./tel_to_csv.sh 2019-10-01 7F7ATR316KER00002
```

## telegraf.conf
The configuration file for telegraf on the InfluxDB server: [/etc/telegraf/telegraf.conf](telegraf.conf)

## [server_optimization.md](server_optimization.md)
Increase The Maximum Number Of Open Files (nginx)

## test_inserts_bulk.js
Inserts num_seconds of second data into vin(s). Vins are hard coded in json files and can be set via the vin_data variable in the test_inserts_bulk.js

`node test_inserts_bulk --year 2019 --month 3 --day 10 --num_seconds 86400`

## test_inserts_per_second.js
Inserts data once per second into vin(s) for num_seconds. Vins are hard coded in json files and can be set via the vin_data variable in the test_inserts_per_second.js

`node test_inserts_per_second --year 2019 --month 3 --day 10 --num_seconds 60`
