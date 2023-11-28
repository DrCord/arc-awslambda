-- insert arcimoto group association remove permission
INSERT INTO user_permission (permission, description) VALUES ('vehicles.vehicle.configuration_write', 'Set configuration for a vehicle');

-- super user group does not get this permission until https://arcimoto.atlassian.net/browse/TEL-740 is resolved
-- INSERT INTO user_permission_group_join (permission, group_id) VALUES ('vehicles.vehicle.configuration_write', (select id from user_group where machine_name='all'));
