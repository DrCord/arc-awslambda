# Utility Functions

Most of the programs here are meant to be run on local machines, unlike those in the lambda directory which are meant to be run in the Arcimoto cloud from within AWS Lambda.

## backfill_from_file.py

Simple utility (based on `influx_backfill.py` and `telemetry_vpc_ingest_influx.py`) to send data into InfluxDB.  
This script is meant to be run on the InfluxDB server.
To use it, the data file must be present on the server, and the `boto3` and `influxdb` modules must be installed within Python3.

## backup_telemetry_analyzer.py

Functions to search through backup telemetry files and determine which files represent close to a full day's worth of telemetry, to within a specified threshold

## export_apis.py

To create a new backup when changes are made to an API endpoint export the API and save it here in version control. [How to export original source info](https://docs.aws.amazon.com/en_pv/apigateway/latest/developerguide/api-gateway-export-api.html)

Use the export_apis.py file in the utility directory.

```sh
python ./utility/export_apis.py --api_names vehicleManager palantir --stage_names dev staging prod
```

### Recognized values for --api_names

- authorityManager
- palantir
- recallsPublic
- vehicleManager
- web

### Recognized values for --stage_names

- dev
- staging
- prod

## grafana_reprovision_group_overviews.py

Reprovision all Grafana vehicle group overview dashboards in the specified environment.

## grafana_reprovision_vehicle_dashboards.py

Reprovision all Grafana vehicle dashboards in the specified environment

## grafana_reprovision_vehicle_groups.py

Reprovision the Grafana vehicle group page in the specified environment.

## influx_backfill.py

Simple utility to take the telemetry contained in a ring buffer file from the Comm module's SD card, and backfill the data to influx. This should not be used for data older than 30 days, since the influxdb retention policy is to get rid of data after 30 days. Use of this utility requires AWS CLI to be installed and authorized, and `boto3` to be installed within Python. (See Arcimoto Wiki: [AWS Command Line Interface](https://sites.google.com/arcimoto.com/wiki/engineering/telematics/arcimoto-cloud/ac-development?authuser=0#h.p_f3rBnh1nhu6L))

### Example usage

In Python:

```python
import influx_backfill

VIN = 'VIN = 7F7ATR312KER00000'
telemetry_file = '2019-09-26_Mark.txt'
influx_backfill.send_telemetry_batch(VIN, telemetry_file)
```

## influx_csv_backup.sh

Script to backup InfluxDB data to a csv file and store it in S3. For this script to work successfully, the EC2 on which it is running (InfluxDB) needs to be able to access the AWS S3 buckets `arcimoto-telemetry` and `arcimoto-telemetry-backup`.  This must be enabled in the telemetry VPC policy, as well as a policy attached to the IAM role assigned to the EC2. Furthermore, the lambda function `ls_vin_to_s3.py` [LAMBDA HAS BEEN REMOVED] should periodically be run automatically in order to create current VIN lists for `influx_csv_backup.sh` to read.  Cloudwatch has a cron-like method for doing this, and currently this is set to create dev, staging, and prod VIN lists once per day and send them to S3.

## parse_metrics.py

Minifies the full metrics.json file

## restore_telemetry_30d.py

Retrieve the last 30 days of telemetry .csv files from S3 and insert them into influxDB, or copy them from a local directory

## telemetry_to_csv.py

Simple utility to take the telemetry contained in a ring buffer file from the Comm module's SD card, and convert the list of JSON objects into a .csv file.

### Python

```python
import telemetry_to_csv

telemetry_file = '2019-09-26_Mark.txt'
save_file = telemetry_file[:-4]+'.csv'
telemetry_to_csv.make_csv(telemetry_file, save_file)
```

### Shell

```sh
telemetry_to_csv.py json_directory csv_directory
```
