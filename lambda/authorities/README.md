# Resource Bundle: Authorities

## References

### Roles

#### authorities.administration

##### Attached Policy

##### Policy Details

#### authorities.public

## Functions

### Administration Functions

- authkey_vehicle_get
  - PERM: authorities.vehicle.read
  - Gets authority related data about a VIN, including authority_ids and factory_pin
- create_authority
  - PERM: authorities.authority.create
  - Creates a new authrority
- delete_authority
  - PERM: authorities.authority.delete
  - Deletes the specified authority, and all sub-authorities below
- rekey_authority
  - PERM: authorities.authority.re-key
  - Regnerates ECDSA key pairs for the specified authority
- provision_vehicle_authority
  - PERM: authorities.authority.provision
  - Delegates authority for a vehicle to the specified authority
- unprovision_vehicle_authority
  - PERM: authorities.authority.unprovision
  - Removed delegated authority from the specified vehicle, and all sub-authorities below

### Public Access Functions

- get_authority
  - PERM: authorities.authority.read
  - Get details about the specified authority, including delegated vehicles, parent, and children
- get_trusted_keys
  - PERM: authorities.public_keys.read
  - Gets a list of all public keys for all delegated authorities for a given VIN
- list_authorities
  - PERM: authorities.authority.read
  - Gets a list of authorities that match given input filters
- sign_vehicle_token
  - PERM: authorities.vehicle.sign
  - PERM: Needs to validate that current user matches the requested authority
  - Takes an input token and generates ECDSA signed token using the given authority