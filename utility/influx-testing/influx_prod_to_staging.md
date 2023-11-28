# How to copy production telemetry database to staging environment
It may be possible to set up the STAGE-InfluxDB server as a child node of InfluxDB, but it is not set up this way now.
To work within this limitation, create a backup on the production server, move it to the staging server, and restore.

## Make backup of prod database on InfluxDB server
On the EC2 InfluxDB, remove any former temporary backup of the DB:
```
\rm /tmp/temp_db_backup/*
```
Create a new one:
```
influxd backup -portable /tmp/temp_db_backup
```

## Pull the production backup to the staging server
On the EC2 STAGE-InfluxDB, remove any former temporary backup of the DB:
```
\rm /tmp/temp_db_backup/*
```
Collect the new one (use sftpinflux alias defined in .bashrc):
```
sftpinflux
get /tmp/temp_db_backup/* /tmp/temp_db_backup/
exit
```

## remove the old databases and replace with new backup
On the EC2 STAGE-InfluxDB, remove existing databases
```
influx
drop database amtelemetry_prod
exit
```
Restore from backup
```
influxd restore -db "amtelemetry" -newdb "amtelemetry_prod" -portable /tmp/temp_db_backup
/tmp/temp_db_backup
```

## play with the data
```
influx -precision rfc3339 -database "amtelemetry_prod"
```
