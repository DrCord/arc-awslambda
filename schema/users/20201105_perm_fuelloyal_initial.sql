-- insert arcimoto group association remove permission
INSERT INTO user_permission (permission, description) VALUES ('fueloyal.user.read', 'Fueloyal: get user data');
INSERT INTO user_permission (permission, description) VALUES ('fueloyal.vehicle.read', 'Fueloyal: get vehicle data');
INSERT INTO user_permission (permission, description) VALUES ('fueloyal.metrics.read', 'Fueloyal: get vehicle data');

-- super user group gets all new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('fueloyal.user.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('fueloyal.vehicle.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('fueloyal.metrics.read', (select id from user_group where machine_name='all'));

-- fueloyal user group needs new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('fueloyal.user.read', (select id from user_group where machine_name='fueloyal'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('fueloyal.vehicle.read', (select id from user_group where machine_name='fueloyal'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('fueloyal.metrics.read', (select id from user_group where machine_name='fueloyal'));
