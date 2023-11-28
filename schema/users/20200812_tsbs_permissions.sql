-- insert tsbs permissions
INSERT INTO user_permission (permission, description) VALUES ('tsbs.tsb.create', 'Create tsb');
INSERT INTO user_permission (permission, description) VALUES ('tsbs.tsb.delete', 'Delete tsb');
INSERT INTO user_permission (permission, description) VALUES ('tsbs.tsb.edit', 'Edit tsb');
INSERT INTO user_permission (permission, description) VALUES ('tsbs.tsb.read', 'Read tsb');
INSERT INTO user_permission (permission, description) VALUES ('tsbs.vehicle.service', 'Mark tsb-ed vehicle serviced');
INSERT INTO user_permission (permission, description) VALUES ('tsbs.vehicle.add', 'Add vehicle to tsb');
INSERT INTO user_permission (permission, description) VALUES ('tsbs.vehicle.edit', 'Edit vehicle tsb');
INSERT INTO user_permission (permission, description) VALUES ('tsbs.vehicle.read', 'Read vehicle tsb');
INSERT INTO user_permission (permission, description) VALUES ('tsbs.vehicle.remove', 'Remove vehicle from tsb');

-- super user group gets all new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.tsb.create', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.tsb.delete', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.tsb.edit', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.tsb.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.vehicle.service', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.vehicle.add', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.vehicle.edit', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.vehicle.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.vehicle.remove', (select id from user_group where machine_name='all'));

-- add permissions to service group
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.vehicle.service', (select id from user_group where machine_name='service'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.vehicle.read', (select id from user_group where machine_name='service'));