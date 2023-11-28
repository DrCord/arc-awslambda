INSERT INTO user_ability (ability, description) VALUES ('Vehicle - Provision', 'Provision a vehicle (and potentially reverse if unroll needed)');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.vehicle.sign', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Provision'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.remove_arcimoto_group', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Provision'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.write', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Provision'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('grafana.group.write', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Provision'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('grafana.vehicle.write', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Provision'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.points.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Provision'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.points.write', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Provision'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.provision', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Provision'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.write', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Provision'));

INSERT INTO user_ability (ability, description) VALUES ('Authority - Create', 'Create an authority');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.create', (SELECT id FROM user_ability WHERE ability = 'Authority - Create'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.read', (SELECT id FROM user_ability WHERE ability = 'Authority - Create'));

INSERT INTO user_ability (ability, description) VALUES ('Fleets Admin', 'All fleets functionality');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.create', (SELECT id FROM user_ability WHERE ability = 'Fleets Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.delete', (SELECT id FROM user_ability WHERE ability = 'Fleets Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.introspect', (SELECT id FROM user_ability WHERE ability = 'Fleets Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.manage-users', (SELECT id FROM user_ability WHERE ability = 'Fleets Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.read', (SELECT id FROM user_ability WHERE ability = 'Fleets Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.write', (SELECT id FROM user_ability WHERE ability = 'Fleets Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('grafana.group.write', (SELECT id FROM user_ability WHERE ability = 'Fleets Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('grafana.vehicle.write', (SELECT id FROM user_ability WHERE ability = 'Fleets Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.read', (SELECT id FROM user_ability WHERE ability = 'Fleets Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Fleets Admin'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicle - Deliver', 'Create authority (optional), sign vehicle token, set GPS on/off, list vehicle and authorities');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.create', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Deliver'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Deliver'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Deliver'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.vehicle.sign', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Deliver'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('odoo.label.print', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Deliver'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.write', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Deliver'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicle - Quality', 'Vehicle Post-Manufacturing Inspection and Certification');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.provision', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Quality'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Quality'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.unprovision', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Quality'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Quality'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('firmware.release-version.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Quality'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('firmware.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Quality'));

INSERT INTO user_ability (ability, description) VALUES ('Authority Admin', 'Access all functionality tied to the Authority Manager API');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.re-key', (SELECT id FROM user_ability WHERE ability = 'Authority Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.create', (SELECT id FROM user_ability WHERE ability = 'Authority Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.delete', (SELECT id FROM user_ability WHERE ability = 'Authority Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.read', (SELECT id FROM user_ability WHERE ability = 'Authority Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Authority Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.vehicle.sign', (SELECT id FROM user_ability WHERE ability = 'Authority Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.remove_arcimoto_group', (SELECT id FROM user_ability WHERE ability = 'Authority Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.write', (SELECT id FROM user_ability WHERE ability = 'Authority Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('grafana.group.write', (SELECT id FROM user_ability WHERE ability = 'Authority Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('grafana.vehicle.write', (SELECT id FROM user_ability WHERE ability = 'Authority Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.points.read', (SELECT id FROM user_ability WHERE ability = 'Authority Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.points.write', (SELECT id FROM user_ability WHERE ability = 'Authority Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.provision', (SELECT id FROM user_ability WHERE ability = 'Authority Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Authority Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.write', (SELECT id FROM user_ability WHERE ability = 'Authority Admin'));

INSERT INTO user_ability (ability, description) VALUES ('Managed Session Admin', 'All Managed Session Functionality');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('managed_session.session.end', (SELECT id FROM user_ability WHERE ability = 'Managed Session Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('managed_session.session.read', (SELECT id FROM user_ability WHERE ability = 'Managed Session Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('managed_session.session.start', (SELECT id FROM user_ability WHERE ability = 'Managed Session Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Managed Session Admin'));

INSERT INTO user_ability (ability, description) VALUES ('Recall Admin', 'Access all functionality tied to Recalls');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.recall.create', (SELECT id FROM user_ability WHERE ability = 'Recall Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.recall.delete', (SELECT id FROM user_ability WHERE ability = 'Recall Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.recall.edit', (SELECT id FROM user_ability WHERE ability = 'Recall Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.recall.read', (SELECT id FROM user_ability WHERE ability = 'Recall Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.vehicle.edit', (SELECT id FROM user_ability WHERE ability = 'Recall Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.vehicle.add', (SELECT id FROM user_ability WHERE ability = 'Recall Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Recall Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.vehicle.remove', (SELECT id FROM user_ability WHERE ability = 'Recall Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.vehicle.service', (SELECT id FROM user_ability WHERE ability = 'Recall Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.updated.read', (SELECT id FROM user_ability WHERE ability = 'Recall Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.updated.write', (SELECT id FROM user_ability WHERE ability = 'Recall Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Recall Admin'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicle - Backfill Telemetry - Engineering', 'List and select vehicle, upload telemetry file for processing and import into telmetry system');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.backfill.engineering', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Backfill Telemetry - Engineering'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Backfill Telemetry - Engineering'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicles - View', 'List vehicles, view individual vehicle data');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicles - View'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicle - Firmware - View', 'Get vehicle firmware');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('firmware.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Firmware - View'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Firmware - View'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicle - Firmware - Edit', 'Get/edit vehicle firmware');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('firmware.release-version.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Firmware - Edit'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('firmware.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Firmware - Edit'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('firmware.vehicle.write', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Firmware - Edit'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Firmware - Edit'));

INSERT INTO user_ability (ability, description) VALUES ('Firmware - Admin', 'Firmware - all functionality');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('firmware.release-version.read', (SELECT id FROM user_ability WHERE ability = 'Firmware - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('firmware.release-version.refresh', (SELECT id FROM user_ability WHERE ability = 'Firmware - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('firmware.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Firmware - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('firmware.vehicle.write', (SELECT id FROM user_ability WHERE ability = 'Firmware - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Firmware - Admin'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicle - GPS Record - View', 'View state of GPS Record toggle');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.re-key', (SELECT id FROM user_ability WHERE ability = 'Vehicle - GPS Record - View'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicle - GPS Record - Set', 'Set state of GPS Record toggle');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - GPS Record - Set'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.write', (SELECT id FROM user_ability WHERE ability = 'Vehicle - GPS Record - Set'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicle - Telemetry Points - Set', 'Set telemetry points that vehicle sends to cloud');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('grafana.vehicle.write', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Telemetry Points - Set'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.metrics.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Telemetry Points - Set'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.points.write', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Telemetry Points - Set'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Telemetry Points - Set'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicle - Telemetry Points - View', 'View telemetry points that vehicle sends to cloud');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.metrics.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Telemetry Points - View'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Telemetry Points - View'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicle - Configuration - View', 'View vehicle manufacturing configuration');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Configuration - View'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicle - Configuration - Set', 'Set vehicle manufactured configuration');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Configuration - Set'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.write', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Configuration - Set'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicle - Sign Token', 'Sign a vehicle token for use to authenticate with a vehicle, user must also have authority over vehicle');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.vehicle.sign', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Sign Token'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Sign Token'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicle Manager Admin', 'All Vehicle related Vehicle Manager API functionality');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.vehicle.sign', (SELECT id FROM user_ability WHERE ability = 'Vehicle Manager Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('firmware.release-version.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle Manager Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('firmware.release-version.refresh', (SELECT id FROM user_ability WHERE ability = 'Vehicle Manager Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('firmware.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle Manager Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('firmware.vehicle.write', (SELECT id FROM user_ability WHERE ability = 'Vehicle Manager Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.write', (SELECT id FROM user_ability WHERE ability = 'Vehicle Manager Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('grafana.group.write', (SELECT id FROM user_ability WHERE ability = 'Vehicle Manager Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('grafana.vehicle.write', (SELECT id FROM user_ability WHERE ability = 'Vehicle Manager Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('managed_session.session.end', (SELECT id FROM user_ability WHERE ability = 'Vehicle Manager Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('managed_session.session.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle Manager Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('managed_session.session.start', (SELECT id FROM user_ability WHERE ability = 'Vehicle Manager Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.backfill.engineering', (SELECT id FROM user_ability WHERE ability = 'Vehicle Manager Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.metrics.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle Manager Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.points.write', (SELECT id FROM user_ability WHERE ability = 'Vehicle Manager Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle Manager Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.write', (SELECT id FROM user_ability WHERE ability = 'Vehicle Manager Admin'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicle - Get Factory PIN', 'Retrieve Vehicle Factory PIN');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Get Factory PIN'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Get Factory PIN'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicle - View Notes', 'View all Notes for vehicles');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - View Notes'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicle - Create Note', 'Create a note for a vehicle');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Create Note'));

INSERT INTO user_ability (ability, description) VALUES ('Users - View', 'List users and view user');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.read', (SELECT id FROM user_ability WHERE ability = 'Users - View'));

INSERT INTO user_ability (ability, description) VALUES ('Users - Admin', 'Users - all functionality');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.read', (SELECT id FROM user_ability WHERE ability = 'Users - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.write', (SELECT id FROM user_ability WHERE ability = 'Users - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.groups.read', (SELECT id FROM user_ability WHERE ability = 'Users - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user-profile.read', (SELECT id FROM user_ability WHERE ability = 'Users - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user-profile.write', (SELECT id FROM user_ability WHERE ability = 'Users - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.create', (SELECT id FROM user_ability WHERE ability = 'Users - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.delete', (SELECT id FROM user_ability WHERE ability = 'Users - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.disable', (SELECT id FROM user_ability WHERE ability = 'Users - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.enable', (SELECT id FROM user_ability WHERE ability = 'Users - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.read', (SELECT id FROM user_ability WHERE ability = 'Users - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.resend_invite', (SELECT id FROM user_ability WHERE ability = 'Users - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.write', (SELECT id FROM user_ability WHERE ability = 'Users - Admin'));

INSERT INTO user_ability (ability, description) VALUES ('Users - Profile - Edit', 'View and edit all user profiles');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user-profile.read', (SELECT id FROM user_ability WHERE ability = 'Users - Profile - Edit'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user-profile.write', (SELECT id FROM user_ability WHERE ability = 'Users - Profile - Edit'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.read', (SELECT id FROM user_ability WHERE ability = 'Users - Profile - Edit'));

INSERT INTO user_ability (ability, description) VALUES ('Users - Create', 'Create user and resend invite');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.create', (SELECT id FROM user_ability WHERE ability = 'Users - Create'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.read', (SELECT id FROM user_ability WHERE ability = 'Users - Create'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.resend_invite', (SELECT id FROM user_ability WHERE ability = 'Users - Create'));

INSERT INTO user_ability (ability, description) VALUES ('Users - Toggle Active', 'Enable and disable user accounts');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.disable', (SELECT id FROM user_ability WHERE ability = 'Users - Toggle Active'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.enable', (SELECT id FROM user_ability WHERE ability = 'Users - Toggle Active'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.read', (SELECT id FROM user_ability WHERE ability = 'Users - Toggle Active'));

INSERT INTO user_ability (ability, description) VALUES ('Permission Groups - View', 'List and view permission groups');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.read', (SELECT id FROM user_ability WHERE ability = 'Permission Groups - View'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.groups.read', (SELECT id FROM user_ability WHERE ability = 'Permission Groups - View'));

INSERT INTO user_ability (ability, description) VALUES ('Odoo - Print Label', 'Send print label request to Odoo printer');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('odoo.label.print', (SELECT id FROM user_ability WHERE ability = 'Odoo - Print Label'));

INSERT INTO user_ability (ability, description) VALUES ('Permission Group - Create', 'Create permission group');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.create', (SELECT id FROM user_ability WHERE ability = 'Permission Group - Create'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.read', (SELECT id FROM user_ability WHERE ability = 'Permission Group - Create'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.groups.read', (SELECT id FROM user_ability WHERE ability = 'Permission Group - Create'));

INSERT INTO user_ability (ability, description) VALUES ('User - Permission Group - Add/Remove', 'Add or remove user from permission group');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.read', (SELECT id FROM user_ability WHERE ability = 'User - Permission Group - Add/Remove'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.write', (SELECT id FROM user_ability WHERE ability = 'User - Permission Group - Add/Remove'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.groups.read', (SELECT id FROM user_ability WHERE ability = 'User - Permission Group - Add/Remove'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.write', (SELECT id FROM user_ability WHERE ability = 'User - Permission Group - Add/Remove'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.users.read', (SELECT id FROM user_ability WHERE ability = 'User - Permission Group - Add/Remove'));

INSERT INTO user_ability (ability, description) VALUES ('Permissions - View', 'List all permissions');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.permissions.read', (SELECT id FROM user_ability WHERE ability = 'Permissions - View'));

INSERT INTO user_ability (ability, description) VALUES ('Permissions Group - Add Permission', 'Add permission to permission group');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.add-permission', (SELECT id FROM user_ability WHERE ability = 'Permissions Group - Add Permission'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.read', (SELECT id FROM user_ability WHERE ability = 'Permissions Group - Add Permission'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.groups.read', (SELECT id FROM user_ability WHERE ability = 'Permissions Group - Add Permission'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.permissions.read', (SELECT id FROM user_ability WHERE ability = 'Permissions Group - Add Permission'));

INSERT INTO user_ability (ability, description) VALUES ('Permissions Group - Remove Permission', 'Remove permission from permission group');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.read', (SELECT id FROM user_ability WHERE ability = 'Permissions Group - Remove Permission'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.remove-permission', (SELECT id FROM user_ability WHERE ability = 'Permissions Group - Remove Permission'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.groups.read', (SELECT id FROM user_ability WHERE ability = 'Permissions Group - Remove Permission'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.permissions.read', (SELECT id FROM user_ability WHERE ability = 'Permissions Group - Remove Permission'));

INSERT INTO user_ability (ability, description) VALUES ('Users - Abilities - List', 'List all user abilities');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.abilities.read', (SELECT id FROM user_ability WHERE ability = 'Users - Abilities - List'));

INSERT INTO user_ability (ability, description) VALUES ('Users - Abilities - Create', 'Create and list all user abilities');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.abilities.create', (SELECT id FROM user_ability WHERE ability = 'Users - Abilities - Create'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.abilities.read', (SELECT id FROM user_ability WHERE ability = 'Users - Abilities - Create'));

INSERT INTO user_ability (ability, description) VALUES ('Permission - Admin', 'All Permission functionality');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.abilities.create', (SELECT id FROM user_ability WHERE ability = 'Permission - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.abilities.read', (SELECT id FROM user_ability WHERE ability = 'Permission - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.add-permission', (SELECT id FROM user_ability WHERE ability = 'Permission - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.create', (SELECT id FROM user_ability WHERE ability = 'Permission - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.delete', (SELECT id FROM user_ability WHERE ability = 'Permission - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.read', (SELECT id FROM user_ability WHERE ability = 'Permission - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.remove-permission', (SELECT id FROM user_ability WHERE ability = 'Permission - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.write', (SELECT id FROM user_ability WHERE ability = 'Permission - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.groups.read', (SELECT id FROM user_ability WHERE ability = 'Permission - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.permissions.read', (SELECT id FROM user_ability WHERE ability = 'Permission - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.users.read', (SELECT id FROM user_ability WHERE ability = 'Permission - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.users.write', (SELECT id FROM user_ability WHERE ability = 'Permission - Admin'));

INSERT INTO user_ability (ability, description) VALUES ('Telemetry - Admin', 'All Telemetry functionality');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.definition.write', (SELECT id FROM user_ability WHERE ability = 'Telemetry - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.metrics.read', (SELECT id FROM user_ability WHERE ability = 'Telemetry - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.points.read', (SELECT id FROM user_ability WHERE ability = 'Telemetry - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.points.write', (SELECT id FROM user_ability WHERE ability = 'Telemetry - Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.version.read', (SELECT id FROM user_ability WHERE ability = 'Telemetry - Admin'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicle - Recalls - Service', 'Service a vehicle for a recall');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.recall.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Recalls - Service'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.vehicle.service', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Recalls - Service'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicle - Recalls - Service'));

INSERT INTO user_ability (ability, description) VALUES ('Vehicles - List with Authorities', 'List all vehicles with associated authority ids');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Vehicles - List with Authorities'));

INSERT INTO user_ability (ability, description) VALUES ('Super Admin', 'Have all permissions');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.create', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.delete', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.provision', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.re-key', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.unprovision', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.public_key.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.vehicle.sign', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.vehicle.unsign_arcimoto', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('firmware.release-version.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('firmware.release-version.refresh', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('firmware.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('firmware.vehicle.write', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.create', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.delete', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.introspect', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.manage-users', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.remove_arcimoto_group', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fueloyal.metrics.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fueloyal.user.create', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fueloyal.user.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fueloyal.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.write', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('grafana.group.write', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('grafana.vehicle.write', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('managed_session.session.end', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('managed_session.session.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('managed_session.session.start', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('model.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('model.write', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('notes.note.delete', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('odoo.label.print', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.recall.create', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.recall.delete', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.recall.edit', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.recall.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.updated.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.updated.write', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.vehicle.add', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.vehicle.edit', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.vehicle.remove', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.vehicle.service', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('sheer_id.verify.dl', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('sheer_id.verify.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.backfill.engineering', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.metrics.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.points.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.points.write', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.version.write', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('telemetry.definition.write', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('tsbs.tsb.create', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('tsbs.tsb.delete', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('tsbs.tsb.edit', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('tsbs.tsb.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('tsbs.vehicle.add', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('tsbs.vehicle.edit', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('tsbs.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('tsbs.vehicle.remove', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('tsbs.vehicle.service', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.abilities.create', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.abilities.delete', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.abilities.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.abilities.update', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.add-permission', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.create', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.delete', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.remove-permission', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.group.write', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.groups.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.permissions.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.preferences.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user-prefs.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user-prefs.write', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user-profile.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user-profile.write', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.create', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.delete', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.disable', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.enable', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.resend_invite', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.user.write', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('users.users.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.provision', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.read', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.self', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.write', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('vehicles.vehicle.configuration_write', (SELECT id FROM user_ability WHERE ability = 'Super Admin'));

INSERT INTO user_ability (ability, description) VALUES ('Authorities List', 'Read all authority data');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('authorities.authority.read', (SELECT id FROM user_ability WHERE ability = 'Authorities List'));

INSERT INTO user_ability (ability, description) VALUES ('Recalls Read', 'Read all recall data');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('recalls.recall.read', (SELECT id FROM user_ability WHERE ability = 'Recalls Read'));

INSERT INTO user_ability (ability, description) VALUES ('Fleets - Read Group', 'Read group for fleet');

INSERT INTO user_ability_permission_join (permission, ability_id) VALUES ('fleets.group.read', (SELECT id FROM user_ability WHERE ability = 'Fleets - Read Group'));