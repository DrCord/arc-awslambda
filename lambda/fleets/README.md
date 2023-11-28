# Resource Bundle: Fleets

## References

### Roles

#### fleets.administration

##### Attached Policy

##### Policy Details

#### fleets.public

## Functions

### Administration Functions

- add_vehicle_to_group
  - PERM: fleets.group.write
  - Adds the requested vehicle to the specified vehicle group
- create_vehicle_group
  - PERM: fleets.group.create
  - Creates a new vehicle group
- delete_vehicle_group
  - PERM: fleets.group.delete
  - Removes the specified vehicle group
- remove_vehicle_from_group
  - PERM: fleets.group.write
  - Removes the requested vehicle from the specified group
- list_vehicle_groups
  - PERM: fleets.group.read
  - Get a list of vehicle groups

### Public Access Functions

- user_groups_get
  - PERM: fleets.group.introspect
  - Get a list of groups (and VINs in that group) permitted to the specified username