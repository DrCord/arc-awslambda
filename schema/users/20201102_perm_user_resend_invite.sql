-- insert arcimoto group association remove permission
INSERT INTO user_permission (permission, description) VALUES ('users.user.resend_invite', 'Resend cognito user creation invitation');

-- super user group gets all new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.user.resend_invite', (select id from user_group where machine_name='all'));
