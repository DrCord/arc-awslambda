-- insert permissions
INSERT INTO user_permission (permission, description) VALUES ('model.read', 'View model data');
INSERT INTO user_permission (permission, description) VALUES ('model.write', 'Write model data');

-- super user group gets all new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('model.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('model.write', (select id from user_group where machine_name='all'));
