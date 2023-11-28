-- insert recalls permissions
INSERT INTO user_permission (permission, description) VALUES ('recalls.recall.create', 'Create recall');
INSERT INTO user_permission (permission, description) VALUES ('recalls.recall.delete', 'Delete recall');
INSERT INTO user_permission (permission, description) VALUES ('recalls.recall.edit', 'Edit recall');
INSERT INTO user_permission (permission, description) VALUES ('recalls.recall.read', 'Read recall');
INSERT INTO user_permission (permission, description) VALUES ('recalls.vehicle.service', 'Mark recalled vehicle serviced');
INSERT INTO user_permission (permission, description) VALUES ('recalls.vehicle.add', 'Add vehicle to recall');
INSERT INTO user_permission (permission, description) VALUES ('recalls.vehicle.edit', 'Edit vehicle recall');
INSERT INTO user_permission (permission, description) VALUES ('recalls.vehicle.read', 'Read vehicle recall');
INSERT INTO user_permission (permission, description) VALUES ('recalls.vehicle.remove', 'Remove vehicle from recall');
INSERT INTO user_permission (permission, description) VALUES ('recalls.updated.read', 'Retrieve last updated datetime for recall data');
INSERT INTO user_permission (permission, description) VALUES ('recalls.updated.write', 'Set last updated datetime for recall data');

-- super user group gets all new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.recall.create', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.recall.delete', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.recall.edit', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.recall.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.vehicle.service', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.vehicle.add', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.vehicle.edit', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.vehicle.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.vehicle.remove', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.updated.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.updated.write', (select id from user_group where machine_name='all'));

-- add permissions to service group
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.vehicle.service', (select id from user_group where machine_name='service'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.vehicle.read', (select id from user_group where machine_name='service'));
