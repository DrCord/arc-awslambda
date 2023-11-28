-- set up recall admin group
INSERT INTO user_group (name, machine_name) VALUES ('Recall Admin', 'recall_admin');

-- permissions for recall admin group
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.recall.create', (select id from user_group where machine_name='recall_admin'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.recall.delete', (select id from user_group where machine_name='recall_admin'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.recall.edit', (select id from user_group where machine_name='recall_admin'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.recall.read', (select id from user_group where machine_name='recall_admin'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.vehicle.service', (select id from user_group where machine_name='recall_admin'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.vehicle.add', (select id from user_group where machine_name='recall_admin'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.vehicle.edit', (select id from user_group where machine_name='recall_admin'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.vehicle.read', (select id from user_group where machine_name='recall_admin'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.vehicle.remove', (select id from user_group where machine_name='recall_admin'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.updated.read', (select id from user_group where machine_name='recall_admin'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('recalls.updated.write', (select id from user_group where machine_name='recall_admin'));

-- set up tsb admin group
INSERT INTO user_group (name, machine_name) VALUES ('TSB Admin', 'tsb_admin');

-- permissions for tsb admin group
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.tsb.create', (select id from user_group where machine_name='tsb_admin'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.tsb.delete', (select id from user_group where machine_name='tsb_admin'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.tsb.edit', (select id from user_group where machine_name='tsb_admin'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.tsb.read', (select id from user_group where machine_name='tsb_admin'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.vehicle.service', (select id from user_group where machine_name='tsb_admin'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.vehicle.add', (select id from user_group where machine_name='tsb_admin'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.vehicle.edit', (select id from user_group where machine_name='tsb_admin'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.vehicle.read', (select id from user_group where machine_name='tsb_admin'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('tsbs.vehicle.remove', (select id from user_group where machine_name='tsb_admin'));