# Resource Bundle: Firmware

## References

### Roles

#### firmware.administration

##### Attached Policy

##### Policy Details

#### firmware.public

## Functions

### Administration Functions

- firmware_version_get_release_data
  - PERM: None
  - Gets current release data from BitBucket. Used in CI pipeline for DeployedFirmware repo.
- firmware_version_refresh
  - PERM: firmware.release-version.refresh
  - Performs roughly the same tasks as firmware_version_get_release_data and firmware_version_set_release_data together: Gets current release data from BitBucket and saves the firmware hashes to the meta table in our DB. This used to be used in our CI pipeline, now seems to be deprecated by the 2 separate functions mentioned.
- firmware_version_set_release_data
  - PERM: None
  - Takes a dictionary of module and firmware hashes and saves to DB. Used to mark the current stable release of vehicle firmware that we fetch and apply to individual vehicles as they are manufactured. Used in CI pipeline for DeployedFirmware repo.

### Public Access Functions

- firmware_version_get
  - PERM: firmware.release-version.read
  - Get currently released version of firmware modules
- firmware_version_vin_get
  - PERM: firmware.vehicle.read
  - Get the currently recorded version of firmware for the given VIN
- firmware_version_vin_set
  - PERM: firmware.vehicle.write
  - Updates the currently recorded versions of firmware for the given VIN
- get_commit_info
  - NOTE: this appears to be hard-coded to Comm Firmware.dfu - DEPRECATED ???