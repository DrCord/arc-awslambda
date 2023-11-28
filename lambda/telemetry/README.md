# Resource Bundle: Telemetry

Functions related to vehicle telemetry access.

## telemetry_vpc_ingest_influx

This lambda uses IoT rules to trigger.

- PROD_telemetryIntake - uses prod alias of lambda to intake telemetry from production vehicles
- STAGE_telemetryIntake - uses staging alias of lambda to intake telemetry from staging vehicles
- DEV_telemetryIntake - uses dev alias of lambda to intake telemetry from dev vehicles
- telemetryIntake_PROD_to_DEV - uses dev alias of lambda to intake telemetry from production vehicles to dev telemetry db with 'DEV-' prefix
