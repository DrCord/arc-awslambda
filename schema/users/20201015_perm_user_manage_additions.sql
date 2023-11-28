-- insert arcimoto group association remove permission
INSERT INTO user_permission (permission, description) VALUES ('users.user.delete', 'Delete a user from the db and cognito, admin use only, not to be attached to API');
INSERT INTO user_permission (permission, description) VALUES ('users.users.read', 'List all users');
INSERT INTO user_permission (permission, description) VALUES ('users.groups.read', 'List all user permission groups');
INSERT INTO user_permission (permission, description) VALUES ('users.permissions.read', 'List all existing user permissions');
INSERT INTO user_permission (permission, description) VALUES ('users.preferences.read', 'List all existing user preferences');

-- super user group gets all new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.user.delete', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.users.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.groups.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.permissions.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.preferences.read', (select id from user_group where machine_name='all'));
