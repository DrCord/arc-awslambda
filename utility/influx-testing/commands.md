# create database
```
CREATE DATABASE amtelemetry
```

# show databases
```
SHOW DATABASES
```

# retention policies (RPs)
```
DROP RETENTION POLICY a_year ON mydb
DROP RETENTION POLICY a_month ON mydb
DROP RETENTION POLICY autogen ON mydb
ALTER RETENTION POLICY "30d" ON "amtelemetry" DEFAULT

CREATE RETENTION POLICY "30d" ON "mydb" DURATION 30d REPLICATION 1 DEFAULT
CREATE RETENTION POLICY "a_month" ON "mydb" DURATION 30d REPLICATION 1 DEFAULT
CREATE RETENTION POLICY "a_year" ON "mydb" DURATION 365d REPLICATION 1
select * from "a_year"."downsampled_data"
SELECT * INTO "60d"."tel_test" FROM "30d"."tel_test" WHERE vin='JRN7FM'
```

# make queries to different retention policies
```
select bms_pack_soc from one_hour.telemetry where vin='DEV-HOVERBOARD'
select bms_pack_soc from "30d".telemetry where vin='DEV-HOVERBOARD'
```
A fully qualified measurement goes as:
```
<"database">.<"retention_policy">.<"measurement">
```

# show data
```
show retention policies
show continuous queries
```

# misc
```
DROP SERIES FROM "tel_test" WHERE vin='D2G1N0'
DROP SERIES FROM "tel_test" WHERE group='xyz'
SELECT * FROM "tel_test" WHERE vin='28EJK1'
```
### grafana:
```
SELECT first(*) FROM "tel_test" WHERE $timeFilter AND vin='JRN7FM' group by time(1m)
```

# group by
```
SELECT mean(speed) AS "mean_speed" FROM "teltest" WHERE vin='D2G1N0' GROUP BY time(1m)
```

# drop all series (danger!)
```
DROP SERIES FROM /.*/
```

# drop a series by vin
```
drop series from "tel_test" where "vin" = '2KDWUL'
```

# count a series by vin
```
SELECT COUNT("speed") FROM "tel_test" WHERE "vin"='2KDWUL
```

# continuous queries (CQs)
```
CREATE CONTINUOUS QUERY dsall ON mydb BEGIN SELECT mean(speed) AS "mean_speed" INTO "a_year"."downsampled_data" FROM "tel_test" WHERE vin='D2G1N0' GROUP BY time(1m) END
```
or for all variables:
downsample with 30 minute averaging from the default RP to the "60d" RP: ("br" in the name refers to "backreferencing"):
```
CREATE CONTINUOUS QUERY "cq_30m_br" ON "amtelemetry" BEGIN SELECT mean(*) INTO "60d".:MEASUREMENT FROM /.*/ GROUP BY time(30m),* END
```
Drop a continuous query:
```
DROP CONTINUOUS QUERY "cq_10m_br" ON "amtelemetry"
```

# test curl post to Influx
Note: This command appears to be deprecated and non-functional.
```
curl -i -XPOST 'http://localhost:8186/telegraf' --data-binary '[{ "speed": 33, "steering_angle": 15, "timestamp": "1552324030269", "vin": "testvin" }, { "speed": 22, "steering_angle": 12, "timestamp": "1552324036368", "vin": "testvin" } ]'
```

# time based query
```
SELECT * FROM "mydb".""."tel_test" WHERE time > '2019-01-01' and time < '2019-12-01T23:59:59Z'
```

# Manual Backup to CSV
```
influx -database 'amtelemetry' -execute 'SELECT * FROM "amtelemetry" WHERE time > '\''2019-10-01'\'' and time < '\''2019-10-02'\'' AND "vin" = 'DEV-ALL_YOUR_BASE' ' -format 'csv' > /opt/exports/out.csv
```

# check server network settings
```
sudo netstat -plntu
```
