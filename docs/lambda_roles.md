# Lambda Execution Roles

All lambdas get the following policy attached to their execution role:

- lambda.default
  - ACTION:
    - logs:CreateLogGroup
    - logs:CreateLogStream
    - logs:PutLogEvents
    - ec2:CreateNetworkInterface
    - ec2:DescribeNetworkInterfaces
    - ec2:DeleteNetworkInterface
  - RESOURCE: *
- sqs.send.message-broker
- secrets.read.user_authentication
  - ACTION: get_secret_value
  - RESOURCE:
    - global.authentication.db.dev
    - global.authentication.db.staging
    - global.authentication.db.prod

## Bundle: Alarms

Incomplete implementation. Bare minimum execution policy until [TEL-370 Health Monitoring](https://arcimoto.atlassian.net/browse/TEL-370) gets to the top of the queue.

- alarms.administration
  - Policy
    - N/A
  - Lambdas
    - monitor_influxdb_backup
    - provision_telemetry_alarm
    - set_db_telemetry_alarm
    - unprovision_telemetry_alarm

## Bundle: Authorities

- authorities.administration
  - Policy
    - secrets.read.db.authorities_administration [WRITE USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - authorities.administration.db.dev
        - authorities.administration.db.staging
        - authorities.administration.db.prod
    - kms.create-encrypt
      - ACTION: Createkey, Encrypt
      - RESOURCE: *
  - Lambdas
    - authkey_vehicle_get
    - create_authority
    - delete_authority
    - factory_pin_generate
    - list_authorities
    - list_vehicles
    - provision_vehicle_authority
    - rekey_authority
    - unprovision_vehicle_authority

- authorities.public
  - Policy
    - secrets.read.db.authorities_public [READ USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - authorities.public.db.dev
        - authorities.public.db.staging
        - authorities.public.db.prod
    - kms.create-encrypt
      - ACTION: Decrypt
      - RESOURCE: *
  - Lambdas
    - get_authority
    - get_trusted_keys
    - sign_vehicle_token

## Bundle: Backfill

- backfill.administration
  - Policy
    - secrets.read.telegraf_endpoint
      - ACTION: get_secret_value
        - RESOURCE:
          - telegraf_endpoint.dev
          - telegraf_endpoint.staging
          - telegraf_endpoint.prod
    - lambda.backfill
      - ACTION: invoke
        - RESOURCE:
          - backfill_ingest_request:dev
          - backfill_ingest_request:staging
          - backfill_ingest_request:prod
          - backfill_notify_complete:dev
          - backfill_notify_complete:staging
          - backfill_notify_complete:prod
          - backfill_notify_failed:dev
          - backfill_notify_failed:staging
          - backfill_notify_failed:prod
          - backfill_s3_delete_file:dev
          - backfill_s3_delete_file:staging
          - backfill_s3_delete_file:prod
          - backfill_s3_load_file:dev
          - backfill_s3_load_file:staging
          - backfill_s3_load_file:prod
    - lambda.default
    - s3.backfill
      - ACTION: PutObject, GetObject, DeleteObject
        - RESOURCE:
          - arn:aws:s3:::arcimoto-backfill/*
    - ses.backfill
      - ACTION: ses:SendEmail
        - RESOURCE:
          - arn:aws:ses:us-west-2:511596272857:identity/no-reply@arcimoto.com
    - step_functions.backfill
      - ACTION: states:StartExecution
        - RESOURCE:
          - arn:aws:states:us-west-2:511596272857:stateMachine:Telemetry_Backfill
  - Lambdas
    - backfill_ingest_request
    - backfill_s3_delete_file
    - backfill_s3_load_file
    - backfill_s3_presigned_url_generate
    - backfill_state_machine_start

## Bundle: Debug

- debug.main
  - Policy
    - cognito.admin-pool.all
      - ACTION: *
      - RESOURCE: *
    - lambda.invoke.all
      - ACTION: invoke
      - RESOURCE: *
    - rds.replicate.main
      - ACTION: CreateDBSnapshot, RestoreDBInstanceFromDBSnapshot, ModifyDBInstance
        - RESOURCE:
          - arn:aws:rds:us-west-2:511596272857:pg:*
          - arn:aws:rds:us-west-2:511596272857:db:telemetryam
          - arn:aws:rds:us-west-2:511596272857:snapshot:*
          - arn:aws:rds:us-west-2:511596272857:secgrp:*
          - arn:aws:rds:us-west-2:511596272857:subgrp:*
          - arn:aws:rds:us-west-2:511596272857:og:*
      - ACTION: DescribeDBSnapshots
        - RESOURCE:
          - arn:aws:rds:us-west-2:511596272857:db:dev-telemetryam
          - arn:aws:rds:us-west-2:511596272857:db:staging-telemetryam
          - arn:aws:rds:us-west-2:511596272857:snapshot:*
      - ACTION: DeleteDBInstance
        - RESOURCE:
          - arn:aws:rds:us-west-2:511596272857:db:dev-telemetryam
          - arn:aws:rds:us-west-2:511596272857:db:staging-telemetryam
          - arn:aws:rds:us-west-2:511596272857:db:unittest-restored
      - ACTION: DescribeDBInstances
        - RESOURCE: *
    - secrets.read.db.debug_main [WRITE USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - debug.main.db.dev
        - debug.main.db.staging
        - debug.main.db.prod
        - debug.main.administration.db.dev
        - debug.main.administration.db.staging
        - debug.main.administration.db.prod
        - telemetryam-sysadmin
        - staging-telemetryam-sysadmin
        - staging-telemetryam-write
        - staging-telemetryam-read
        - dev-telemetryam-sysadmin
        - dev-telemetryam-write
        - dev-telemetryam-read
    - secrets.read.unittest.users.tokens
      - ACTION: get_secret_value
      - RESOURCE:
        - unittest.users.tokens
    - s3.debug.main
      - ACTION: s3:PutObject, DeleteObject
      - RESOURCE:
        - arcimoto-backfill
  - Lambdas
    - debug_set_cognito_user_mfa
    - debug_update_cognito_user
    - util_telemetry_execute_sql

- debug.authority
  - Policy
    - secrets.read.db.debug_authority
      - ACTION: get_secret_value
      - RESOURCE:
        - debug.authority.db.dev
        - debug.authority.db.staging
        - debug.authority.db.prod
    - secrets.read.unittest.users.tokens
      - ACTION: get_secret_value
      - RESOURCE:
        - unittest.users.tokens
  - Lambdas
    - util_authkey_execute_sql

## Bundle: Firmware

- firmware.administration
  - Policy
    - secrets.read.bitbucket.firmware_administration
      - ACTION: get_secret_value
      - RESOURCE: bitbucket.api
    - secrets.read.db.firmware_administration [WRITE USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - firmware.administration.db.dev
        - firmware.administration.db.staging
        - firmware.administration.db.prod
  - Lambdas
    - firmware_version_get_release_data
    - firmware_version_refresh
    - firmware_version_vin_set
    - firmware_version_set_release_data
    - firmware_version_vin_set
- firmware.public
  - Policy
    - secrets.read.db.firmware_public [READ USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - firmware.public.db.dev
        - firmware.public.db.staging
        - firmware.public.db.prod
    - secrets.read.bitbucket.firmware_public
      - ACTION: get_secret_value
      - RESOURCE: bitbucket.api
  - Lambdas
    - firmware_version_get
    - firmware_version_vin_get
    - get_commit_info

## Bundle: Fleets

- fleets.administration
  - Policy
    - secrets.read.db.fleets_administration [WRITE USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - fleets.administration.db.dev
        - fleets.administration.db.staging
        - fleets.administration.db.prod
  - Lambdas
    - add_vehicle_to_group
    - create_vehicle_group
    - delete_vehicle_group
    - fleets_vehicle_group_add_user
    - fleets_vehicle_group_remove_user
    - list_vehicle_groups
    - remove_vehicle_from_group
- fleets.public
  - Policy
    - secrets.read.db.fleets_public [READ USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - fleets.public.db.dev
        - fleets.public.db.staging
        - fleets.public.db.prod
  - Lambdas
    - get_vehicle_group
    - user_groups_get

## Bundle: Fueloyal

- fueloyal.administration
  - Policy
    - secrets.read.db.fueloyal_administration [WRITE USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - fueloyal.administration.db.dev
        - fueloyal.administration.db.staging
        - fueloyal.administration.db.prod
  - Lambdas
    - TODO
- fueloyal.public
  - Policy
    - secrets.read.db.fueloyal_public [READ USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - fueloyal.public.db.dev
        - fueloyal.public.db.staging
        - fueloyal.public.db.prod
    - s3.read.fueloyal_public
      - ACTION:
        - s3:GetObject
        - s3:GetObjectVersion
      - RESOURCE:
        - arn:aws:s3:::arcimoto-telemetry/*
  - Lambdas
    - TODO

## Bundle: Grafana

- grafana.administration
  - Policy
    - secrets.read.grafana.grafana_administration
      - ACTION: get_secret_value
      - RESOURCE: grafana.api
    - secrets.read.db.grafana_administration [READ USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - grafana.administration.db.dev
        - grafana.administration.db.staging
        - grafana.administration.db.prod
  - Lambdas
    - provision_grafana_groups
    - provision_grafana_overview
    - provision_grafana_vehicle

## Bundle: Hologram

- hologram.administration
  - Policy
    - secrets.read.hologram.hologram_administration
      - ACTION: get_secret_value
      - RESOURCE: hologram.api
    - sqs.read.hologram.change_plan
      - ACTION:
        - DeleteMessage
        - GetQueueUrl
        - ReceiveMessage
        - GetQueueAttributes
      - RESOURCE:
        - hologram_change_plan_dev
        - hologram_change_plan_staging
        - hologram_change_plan_prod
    - sqs.write.hologram.change_plan
      - ACTION: SendMessage
      - RESOURCE:
        - hologram_change_plan_dev
        - hologram_change_plan_staging
        - hologram_change_plan_prod
    - sqs.read.hologram.update_device
      - ACTION:
        - DeleteMessage
        - ReceiveMessage
        - GetQueueAttributes
      - RESOURCE:
        - dev_update_hologram_device
        - stage_update_hologram_device
        - prod_update_hologram_device
  - Lambdas
    - hologram_change_plan
    - hologram_check_plans
    - update_hologram

## Bundle: Managed Session

- managed_session.administration
  - Policy
    - secrets.read.db.managed_session_administration [WRITE USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - managed_session.administration.db.dev
        - managed_session.administration.db.staging
        - managed_session.administration.db.prod
    - secrets.read.db.telegraf_endpoint
      - ACTION: get_secret_value
      - RESOURCE:
        - telegraf_endpoint.dev
        - telegraf_endpoint.staging
        - telegraf_endpoint.prod
  - Lambdas
    - managed_session_end
    - managed_session_get
    - managed_session_list
    - managed_session_mode_set
    - managed_session_start
    - managed_session_telemetry_get

## Bundle: Notes

- notes.administration
  - Policy
    - secrets.read.db.notes_administartion [WRITE USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - notes.administration.db.dev
        - notes.administration.db.staging
        - notes.administration.db.prod
  - Lambdas
    - note_delete

- notes.public
  - Policy
    - secrets.read.db.notes_public [WRITE USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - notes.public.db.dev
        - notes.public.db.staging
        - notes.public.db.prod
  - Lambdas
    - note_create
    - notes_get

## Bundle: Recalls

- recall.administration
  - Policy
    - secrets.read.db.recall_administration [WRITE USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - recall.administration.db.dev
        - recall.administration.db.staging
        - recall.administration.db.prod
  - Lambdas
    - recall_add_vehicle
    - recall_create
    - recall_delete
    - recall_edit_vehicle
    - recall_edit
    - recall_get
    - recall_list
    - recall_remove_vehicle
    - recall_service_vehicle
    - recall_set_updated
    - remedy_create
    - remedy_delete
    - remedy_edit
    - remedy_list

- recall.public
  - Policy
    - secrets.read.db.recall_public [READ USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - recall.public.db.dev
        - recall.public.db.staging
        - recall.public.db.prod
  - Lambdas
    - recall_get_updated
    - recall_get_vehicle
    - recall_list_vehicle
    - remedy_get

## Bundle: SheerId

- sheer_id.public
  - Policy
    - secrets.read.sheer_id_public
  - Lambdas
    - sheer_id_verify_dl

## Bundle: Telemetry

- telemetry.administration
  - Policy
    - s3.write.telemetry_administration
      - ACTION: put_object
      - RESOURCE: arcimoto-telemetry
    - secrets.read.db.telemetry_administration [WRITE USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - telemetry.administration.db.dev
        - telemetry.administration.db.staging
        - telemetry.administration.db.prod
  - Lambdas
    - add_telemetry_definition
    - set_telemetry_points
    - set_telemetry_version

- telemetry.public
  - Policy
    - s3.read.telemetry_public
      - ACTION: get_object
      - RESOURCE: arcimoto-telemetry
    - secrets.read.db.telemetry_public [READ USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - telemetry.public.db.dev
        - telemetry.public.db.staging
        - telemetry.public.db.prod
    - secrets.read.influx_ip [READ USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - influx_ip.dev
        - influx_ip.staging
        - influx_ip.prod
    - secrets.read.telegraf_endpoint [READ USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - telegraf_endpoint.dev
        - telegraf_endpoint.staging
        - telegraf_endpoint.prod
    - iot.write.telemetry_public
      - ACTION:
        - publish (/vehicles/{}/telemetry/defs)
      - RESOURCE:
        - /vehicles/{}/telemetry/defs
  - Lambdas
    - get_telemetry_definition
    - get_telemetry_metrics_keys
    - get_telemetry_points
    - telemetry_points_get_defaults
    - vehicles_telemetry_get

## Bundle: Tests

- debug.administration
  - Policy
    - See Bundle: Debug
  - Lambdas
    - TODO: TEL-488

## BUNDLE: Userpool

- userpool.administration
  - Policy
    - ses.userpool
      - ACTION
        - ses:SendEmail
      - RESOURCE
        - no-reply@arcimoto.com
    - cognito_user_pools.userpool
      - ACTION
        - cognito-idp:AdminListGroupsForUser
      - RESOURCE
        - us-west-2_3x5jXoVFD

## Bundle: Users

- users.administration
  - Policy
    - cognito.admin-pool.all
      - ACTION: *
      - RESOURCE: *
    - secrets.read.db.users_administration [WRITE USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - users.administration.db.dev
        - users.administration.db.staging
        - users.administration.db.prod
  - Lambdas
    - users_add_permission_to_group
    - users_add_user_to_group
    - users_create_user
    - users_disable_user
    - users_enable_user
    - users_group_create
    - users_group_delete
    - users_permissions_ability_create
    - users_remove_permission_from_group
    - users_remove_user_from_group

- users.public
  - Policy
    - cognito.update-user.all
      - cognito.update-user.all
        - ACTION: admin_update_user_attributes
        - RESOURCE: *
    - cognito.get-user.all
      - cognito.get-user.all
        - ACTION: admin_get_user
        - RESOURCE: *
    - secrets.read.users_public_db_dev [REPLACE]
      - ACTION: get_secret_value
      - RESOURCE:
        - users.public.db.dev
        - users.public.db.staging
        - users.public.db.prod
  - Lambdas
    - users_group_get
    - users_profile_get
    - users_profile_update
    - users_user_get
    - users_permissions_abilities_list

## Bundle: Utility

- utility.administration
  - Policy
    - s3.write.utility_administration
      - ACTION:
        - put_object (arcimoto-telemetry-backup)
        - get_object (arcimoto-telemetry)
        - head_object (arcimoto-telemetry-backup)
      - RESOURCE:
        - arcimoto-telemetry-backup
        - arcimoto-telemetry
    - lambda.invoke.all
      - ACTION: invoke
      - RESOURCE: *
    - secrets.read.slack.utility_administration
      - ACTION: get_secret_value
      - RESOURCE: slack.api
    - sns.write.utility_administration
      - ACTION:
        - publish (lambda_notifications)
      - RESOURCE:
        - lambda_notifications
    - sqs.read.utility_administration
      - ACTION:
        - DeleteMessage
        - ReceiveMessage
        - GetQueueAttributes
      - RESOURCE:
        - arcimoto_notifications_dev
        - arcimoto_notifications_staging
        - arcimoto_notifications
    - cloudwatch.read.utility_administration
      - ACTION: get_log_events
      - RESOURCE:
        - GROUP: DEV-influx-csv-backup
        - GROUP: STAGE-influx_csv_backup
        - GROUP: influx_csv_backup
        - STREAM: i-0aea13793a77d647d (dev)
        - STREAM: i-046d48b26d0fd82ca (staging)
        - STREAM: i-003cc9f4047edc985 (prod)
  - Lambdas
    - message_broker
    - set_continuous_queries
    - step_wrapper

- utility.basic
  - Policy
    - N/A
  - Lambdas
    - filter_2000_timestamps
    - print_label_request

## Bundle: Vehicles

- vehicles.administration
  - Policy
    - secrets.read.db.vehicles_administration [WRITE USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - vehicles.administration.db.dev
        - vehicles.administration.db.staging
        - vehicles.administration.db.prod
    - iot.read.vehicles_administration
      - ACTION:
        - list_attached_policies
        - list_thing_principals
        - describe_thing
        - list_thing_groups_for_thing
      - RESOURCE: *
    - iot.write.vehicles_administration
      - ACTION:
        - detach_policy
        - detach_thing_principal
        - update_certificate
        - delete_certificate
        - create_keys_and_certificate
        - attach_thing_principal
        - attach_policy
        - create_thing
        - add_thing_to_thing_group
        - delete_thing
      - RESOURCE: *
  - Lambdas
    - add_vehicle_metadata
    - get_telemetry_vehicle
    - list_telemetry_vehicles
    - provision_iot_certificate
    - provision_iot
    - provision_vehicle_telemetry
    - unprovision_iot_certificate
    - unprovision_iot
    - unprovision_vehicle_telemetry
    - vehicles_configuration_set
    - vehicles_options_set
    - vehicles_vehicle_part_set

- vehicles.public
  - Policy
    - secrets.write.db.vehicles_public [WRITE USER]
      - ACTION: get_secret_value
      - RESOURCE:
        - vehicles.public.db.dev
        - vehicles.public.db.staging
        - vehicles.public.db.prod
    - iot.read.vehicles_public
      - ACTION:
        - READ get_thing_shadow
      - RESOURCE: *
    - iot.write.vehicles_public
      - ACTION:
        - publish (/vehicles/{}/shadow/desired)
        - update_thing_shadow (*)
      - RESOURCE:
        - /vehicles/{}/shadow/desired
    - lambda.invoke.vehicles_public
      - ACTION: invoke
      - RESOURCE:
        - firmware_version_get
        - firmware_version_vin_set
        - get_trusted_keys
    - s3.read.vehicles_public
      - ACTION: get_object
      - RESOURCE: argimoto-telemetry
  - Lambdas
    - get_vehicle_shadow
    - gps_privacy_setting_get
    - gps_recording_toggle
    - register_vehicle
    - shadow_reported_state
    - update_shadow_document
    - vehicles_vehicle_shadow_synchronized
