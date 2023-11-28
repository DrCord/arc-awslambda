-- this must be run after 20200527A_user_group_alters.sql as it requires the alters to table structure in that file

-- truncate and reset counter for user_group, user_permission, user_permission_group_join tables
TRUNCATE user_group, user_permission, user_permission_group_join RESTART IDENTITY CASCADE;

-- insert all the permissions
INSERT INTO user_permission (permission, description) VALUES ('authorities.vehicle.read', 'Ability to read vehicle authority information about a vehicle');
INSERT INTO user_permission (permission, description) VALUES ('authorities.authority.create', 'Ability to create an authority');
INSERT INTO user_permission (permission, description) VALUES ('authorities.authority.delete', 'Ability to delete an authority');
INSERT INTO user_permission (permission, description) VALUES ('authorities.authority.re-key', 'Ability to regenerate the key pair for an authority');
INSERT INTO user_permission (permission, description) VALUES ('authorities.authority.provision', 'Ability to delegate authority to a vehicle');
INSERT INTO user_permission (permission, description) VALUES ('authorities.authority.unprovision', 'Ability to remove authority from a vehicle');
INSERT INTO user_permission (permission, description) VALUES ('authorities.authority.read', 'Ability to read authority information');
INSERT INTO user_permission (permission, description) VALUES ('authorities.public_key.read', 'Ability to read the public key of an authority');
INSERT INTO user_permission (permission, description) VALUES ('authorities.vehicle.sign', 'Ability to sign a token for vehicle access with an authority');
INSERT INTO user_permission (permission, description) VALUES ('users.user.create', 'Ability to create new users');
INSERT INTO user_permission (permission, description) VALUES ('users.user.disable', 'Ability to disable existing users');
INSERT INTO user_permission (permission, description) VALUES ('users.user.enable', 'Ability to enable existing users');
INSERT INTO user_permission (permission, description) VALUES ('users.user.write', 'Ability to edit existing users');
INSERT INTO user_permission (permission, description) VALUES ('users.user.read', 'Ability to read users');
INSERT INTO user_permission (permission, description) VALUES ('users.group.create', 'Ability to create new groups');
INSERT INTO user_permission (permission, description) VALUES ('users.group.write', 'Ability to add/remove users to/from groups');
INSERT INTO user_permission (permission, description) VALUES ('users.group.delete', 'Ability to delete groups');
INSERT INTO user_permission (permission, description) VALUES ('users.group.add-permission', 'Ability to add permission to group');
INSERT INTO user_permission (permission, description) VALUES ('users.group.remove-permission', 'Ability to remove permission from group');
INSERT INTO user_permission (permission, description) VALUES ('users.group.read', 'Ability to read group');
INSERT INTO user_permission (permission, description) VALUES ('users.user-profile.read', 'Ability to read user profile');
INSERT INTO user_permission (permission, description) VALUES ('users.user-profile.write', 'Ability to edit user profile');
INSERT INTO user_permission (permission, description) VALUES ('users.user-prefs.read', 'Ability to read user preferences');
INSERT INTO user_permission (permission, description) VALUES ('users.user-prefs.write', 'Ability to edit user preferences');
INSERT INTO user_permission (permission, description) VALUES ('firmware.release-version.refresh', 'Ability to re-fetch current firmware versions from BitBucket');
INSERT INTO user_permission (permission, description) VALUES ('firmware.release-version.read', 'Ability to read released version of module firmware');
INSERT INTO user_permission (permission, description) VALUES ('firmware.vehicle.read', 'Ability to read current firmware versions for vehicle');
INSERT INTO user_permission (permission, description) VALUES ('firmware.vehicle.write', 'Ability to update current firmware versions for vehicle');
INSERT INTO user_permission (permission, description) VALUES ('fleets.group.write', 'Ability to add/remove vehicles to/from vehicle groups');
INSERT INTO user_permission (permission, description) VALUES ('fleets.group.create', 'Ability to create vehicle groups');
INSERT INTO user_permission (permission, description) VALUES ('fleets.group.delete', 'Ability to remove vehicle groups');
INSERT INTO user_permission (permission, description) VALUES ('fleets.group.read', 'Ability to read vehicle groups');
INSERT INTO user_permission (permission, description) VALUES ('fleets.group.introspect', 'Ability to discover all groups and vehicles accessible by a given username');
INSERT INTO user_permission (permission, description) VALUES ('grafana.group.write', 'Ability to add/remove vehicles to/from grafana groups');
INSERT INTO user_permission (permission, description) VALUES ('grafana.vehicle.write', 'Ability to update grafanay vehicle dashboards');
INSERT INTO user_permission (permission, description) VALUES ('vehicles.vehicle.write', 'Ability to edit vehicle details');
INSERT INTO user_permission (permission, description) VALUES ('vehicles.vehicle.provision', 'Ability to provision vehicle');
INSERT INTO user_permission (permission, description) VALUES ('vehicles.vehicle.read', 'Ability to read vehicle information');
INSERT INTO user_permission (permission, description) VALUES ('vehicles.vehicle.self', 'Permission for vehicle to self-report data');

-- set up super user group
INSERT INTO user_group (name, machine_name) VALUES ('Administrator', 'all');

-- super user group gets everything
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.authority.create', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.authority.delete', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.authority.re-key', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.authority.provision', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.authority.unprovision', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.authority.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.public_key.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.vehicle.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.vehicle.sign', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.user.create', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.user.disable', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.user.enable', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.user.write', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.user.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.group.create', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.group.write', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.group.delete', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.group.add-permission', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.group.remove-permission', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.group.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.user-profile.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.user-profile.write', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.user-prefs.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.user-prefs.write', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('firmware.release-version.refresh', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('firmware.release-version.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('firmware.vehicle.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('firmware.vehicle.write', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('fleets.group.write', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('fleets.group.create', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('fleets.group.delete', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('fleets.group.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('fleets.group.introspect', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('grafana.group.write', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('grafana.vehicle.write', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('vehicles.vehicle.write', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('vehicles.vehicle.provision', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('vehicles.vehicle.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('vehicles.vehicle.self', (select id from user_group where machine_name='all'));

-- set up provision group
INSERT INTO user_group (name, machine_name) VALUES ('Provision', 'provision');

-- permissions for provision group
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('vehicles.vehicle.provision', (select id from user_group where machine_name='provision'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('grafana.vehicle.write', (select id from user_group where machine_name='provision'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.authority.provision', (select id from user_group where machine_name='provision'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('grafana.group.write', (select id from user_group where machine_name='provision'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('fleets.group.write', (select id from user_group where machine_name='provision'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('vehicles.vehicle.self', (select id from user_group where machine_name='provision'));

-- set up delivery group
INSERT INTO user_group (name, machine_name) VALUES ('Delivery', 'delivery');

-- permissions for delivery group
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('vehicles.vehicle.read', (select id from user_group where machine_name='delivery'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.vehicle.read', (select id from user_group where machine_name='delivery'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.authority.create', (select id from user_group where machine_name='delivery'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.authority.read', (select id from user_group where machine_name='delivery'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.authority.provision', (select id from user_group where machine_name='delivery'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('vehicles.vehicle.self', (select id from user_group where machine_name='delivery'));

-- set up quality group
INSERT INTO user_group (name, machine_name) VALUES ('Quality', 'quality');

-- permissions for quality group
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('vehicles.vehicle.read', (select id from user_group where machine_name='quality'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('firmware.vehicle.read', (select id from user_group where machine_name='quality'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.authority.provision', (select id from user_group where machine_name='quality'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.authority.unprovision', (select id from user_group where machine_name='quality'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('vehicles.vehicle.self', (select id from user_group where machine_name='quality'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.vehicle.sign', (select id from user_group where machine_name='quality'));

-- set up Service group
INSERT INTO user_group (name, machine_name) VALUES ('Arcimoto Service', 'service');

-- permissions for service group
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('vehicles.vehicle.read', (select id from user_group where machine_name='service'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('firmware.vehicle.read', (select id from user_group where machine_name='service'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('firmware.vehicle.write', (select id from user_group where machine_name='service'));

-- set up Support group
INSERT INTO user_group (name, machine_name) VALUES ('Arcimoto Support', 'support');

-- permissions for support group
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('vehicles.vehicle.read', (select id from user_group where machine_name='support'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('firmware.vehicle.read', (select id from user_group where machine_name='support'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.vehicle.read', (select id from user_group where machine_name='support'));
