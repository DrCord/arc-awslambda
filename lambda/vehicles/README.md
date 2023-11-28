# Resource Bundle: Vehicles

## References

### Roles

#### vehicles.administration

#### vehicles.provision

#### vehicles.self

## Functions

- add_vehicle_metadata
  - PERM: vehicles.vehicle.write
- factory_pin_generate
  - PERM: vehicles.vehicle.provision
- get_telemtry_vehicle
  - PERM: vehicles.vehicle.read
- get_vehicle_shadow
  - PERM: vehicles.vehicle.read
- gps_privacy_setting_get
  - PERM: vehicles.vehicle.read
- gps_recording_toggle
  - PERM: vehicles.vehicle.write
- list_telemetry_vehicles
  - PERM: vehicles.vehicle.read
- provision_iot_certificate
  - PERM: vehicles.vehicle.provision
- provision_iot
  - PERM: vehicles.vehicle.provision
- provision_vehicle_authority
  - PERM: authorities.authorities.provision
- provision_vehicle_telemetry
  - PERM: vehicles.vehicle.provision
- register_vehicle
  - PERM: vehicles.vehicle.self
- shadow_reported_state
  - PERM: vehicles.vehicle.self
- unprovision_iot_certificate
  - PERM: vehicles.vehicle.provision
- unprovision_iot
  - PERM: vehicles.vehicle.provision
- unprovision_vehicle_telemetry
  - PERM: vehicles.vehicle.provision
- update_shadow_document
  - PERM: vehicles.vehicle.self
- vehicles_option_set
  - PERM: vehicles.vehicle.provision