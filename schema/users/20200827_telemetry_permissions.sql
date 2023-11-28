-- insert notes permissions
INSERT INTO user_permission (permission, description) VALUES ('telemetry.definition.write', 'Telemetry definitions - add');
INSERT INTO user_permission (permission, description) VALUES ('telemetry.metrics.read', 'Telemetry definitions - add');
INSERT INTO user_permission (permission, description) VALUES ('telemetry.points.read', 'Telemetry definitions - add');
INSERT INTO user_permission (permission, description) VALUES ('telemetry.points.write', 'Telemetry definitions - add');
INSERT INTO user_permission (permission, description) VALUES ('telemetry.version.write', 'Telemetry definitions - add');

-- super user group gets all new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('telemetry.definition.write', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('telemetry.metrics.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('telemetry.points.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('telemetry.points.write', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('telemetry.version.write', (select id from user_group where machine_name='all'));
