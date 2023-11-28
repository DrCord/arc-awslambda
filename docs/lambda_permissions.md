# Lambda Permissions

## Bundle: Alarms

- monitor_influxdb_backup
- provision_telemetry_alarm
- set_db_telemetry_alarm
- unprovision_telemetry_alarmunset_db_telemetry_alarm

## Bundle: Authorities

- authkey_vehicle_get
  - authorities.vehicle.read
- create_authority
  - authorities.authority.create
- delete_authority
  - authorities.authority.delete
- factory_pin_generate
  - vehicles.vehicle.provision
- get_authority
  - authorities.authority.read
- get_trusted_keys
  - None
- list_authorities
  - authorities.authority.read
- list_vehicles
  - authorities.vehicle.read
- provision_vehicle_authority
  - authorities.vehicle.sign
- rekey_authority
  - authorities.authority.re-key
- sign_vehicle_token
  - authorities.vehicle.sign
- unprovision_vehicle_authority
  - authorities.vehicle.sign

## Bundle: Backfill

- backfill_ingest_request
  - telemetry.backfill.engineering
- backfill_s3_delete_file
  - telemetry.backfill.engineering
- backfill_s3_load_file
  - telemetry.backfill.engineering
- backfill_notify_complete
  - None
- backfill_notify_failed
  - None
- backfill_s3_presigned_url_generate
  - telemetry.backfill.engineering
- backfill_state_machine_start
  - telemetry.backfill.engineering

## Bundle: Debug

- debug_set_cognito_user_mfa
- debug_update_cognito_user
- util_telemetry_execute_sql
- util_authkey_execute_sql
- util_authkey_execute_sql

## Bundle: Firmware

- firmware_version_get
  - firmware.release-version.read
- firmware_version_get_release_data
  - None: runs in pipeline
- firmware_version_refresh
  - firmware.release-version.refresh
- firmware_version_set_release_data
  - None: runs in pipeline
- firmware_version_vin_get
  - firmware.vehicle.read
- firmware_version_vin_set
  - firmware.vehicle.write
- get_commit_info
  - firmware.release-version.read

## Bundle: Fleets

- add_vehicle_to_group
  - fleets.group.write
- create_vehicle_group
  - fleets.group.create
- delete_vehicle_group
  - fleets.group.delete
- fleets_vehicle_group_add_user
  - fleets.group.write
- fleets_vehicle_group_remove_user
  - fleets.group.write
- get_vehicle_group
  - fleets.group.read
- list_vehicle_groups
  - fleets.group.read
- remove_vehicle_from_arcimoto_group
  - fleets.group.remove_arcimoto_group
- remove_vehicle_from_group
  - fleets.group.write
- user_groups_get
  - fleets.group.read

## Bundle: Fueloyal

- fl_user_get
  - no permissions
  ALT: if username != arcimoto.user.current().username:
  - fueloyal.user.read
- fl_user_get
  - fueloyal.vehicle.read

## Bundle: Grafana

- provision_grafana_groups
  - grafana.group.write
- provision_grafana_overview
  - grafana.group.write
  - grafana.vehicle.write
- provision_grafana_vehicle
  - grafana.vehicle.write

## Bundle: Hologram

- hologram_change_plan
- hologram_check_plans
- update_hologram

## Bundle: Managed Session

- managed_session_end
  - managed_session.session.end
- managed_session_get
  - managed_session.session.read
- managed_session_list
  - managed_session.session.read
- managed_session_mode_set
  - vehicles.vehicle.provision
- managed_session_start
  - managed_session.session.start
- managed_session_telemetry_get
  - managed_session.session.read

## Bundle: Notes

- note_create
  - no specific permission required
- note_delete
  - notes.note.delete
- notes_get
  - no specific permission required

## Bundle: Recalls

- recall_add_vehicle
  - recalls.vehicle.add
- recall_create
  - recalls.recall.create
- recall_delete
  - recalls.recall.delete
- recall_edit
  - recalls.recall.edit
- recall_edit_vehicle
  - recalls.vehicle.edit
- recall_get
  - recalls.recall.read
- recall_get_updated
  - None
- recall_get_vehicle
  - recalls.vehicle.read
- recall_list
  - recalls.recall.read
- recall_list_vehicle
  - no permissions
  ALT: if args.get_deleted_recalls == True
  - recalls.recall.read
- recall_remove_vehicle
  - recalls.vehicle.remove
- recall_service_vehicle
  - recalls.vehicle.service
- recall_set_updated
  - recalls.updated.write
- remedy_create
  - recalls.recall.create
  - recalls.recall.edit
- remedy_delete
  - recalls.recall.edit
  - recalls.recall.delete
- remedy_edit
  - recalls.recall.edit
- remedy_get
  - recalls.recall.read
- remedy_list
  - recalls.recall.read

## Bundle: Telemetry

- add_telemetry_definition
  - telemetry.definition.write
- get_telemetry_definition
  - no permissions
- get_telemetry_metrics_keys
  - telemetry.metrics.read
- get_telemetry_points
  - telemetry.points.read
- set_telemetry_points
  - telemetry.points.write
- set_telemetry_version
  - telemetry.version.write
- telemetry_points_get_defaults
  - telemetry.points.read
- vehicles_telemetry_get
  - no permissions

## Bundle: Tests

## Bundle: Userpool

- userpool_post_confirmation
  - userpool.administration

## Bundle: Users

- users_add_permission_to_group
  - users.group.add-permission
- users_add_user_to_group
  - users.group.write
  - users.user.write
- users_create_user
  - users.user.create
- users_delete_user
  - users.user.delete
- users_disable_user
  - users.user.disable
- users_enable_user
  - users.user.enable
- users_group_create
  - users.group.create
- users_group_delete
  - users.group.delete
- users_group_get
  - users.group.read
- users_groups_list
  - users.groups.read
- users_remove_permission_from_group
  - users.group.remove-permission
- users_remove_user_from_group
  - users.group.write
  - users.user.write
- users_permissions_abilities_list
  - users.abilities.read
- users_permissions_ability_create
  - users.abilities.create
- users_permissions_list
  - users.permissions.read
- users_preferences_list
  - None
- users_profile_get
  - no permissions
  ALT: if args.username != arcimoto.user.current().username
  - users.user-profile.read
- users_profile_update
  - no permissions
  ALT: if args.username != arcimoto.user.current().username
  - users.user-profile.write
- users_resend_user_invite
  - users.user.resend_invite
- users_user_get
  ALT: if args.username != arcimoto.user.current().username
  - users.user.read
- users_users_list
  - users.users.read

## Bundle: Utility

- message_broker
  - no permission
- print_label_request
  - odoo.label.print
- set_continuous_queries
- step_wrapper
  - no permission
- utility_release_data_migration
  - no permission

## Bundle: Vehicles

- add_vehicle_metadata
  - vehicles.vehicle.write
- get_vehicle_shadow
- get_telemetry_vehicle
  - None
  ALT: if not arcimoto.vehicle.Vehicle(vin).validate_user_access(current_user.username)
  - vehicles.vehicle.read
- get_vehicle_shadow
  - None
- gps_privacy_setting_get
  - vehicles.vehicle.read
- gps_recording_toggle
  - vehicles.vehicle.write
- list_telemetry_vehicles
  - vehicles.vehicle.read
- provision_iot_certificate
  - vehicles.vehicle.provision
- provision_iot
  - vehicles.vehicle.provision
- provision_vehicle_telemetry
  - vehicles.vehicle.provision
- register_vehicle
- shadow_reported_state
- unprovision_iot_certificate
  - vehicles.vehicle.provision
- unprovision_iot
  - vehicles.vehicle.provision
- unprovision_vehicle_telemetry
  - vehicles.vehicle.provision
- update_shadow_document
  - None
- vehicles_configuration_set
  - vehicles.vehicle.write
- vehicles_options_set
  - vehicles.vehicle.write
- vehicles_vehicle_part_set
  - vehicles.vehicle.write
- vehicles_vehicle_shadow_synchronized
  - vehicles.vehicle.read
