-- insert permissions
INSERT INTO user_permission (permission, description) VALUES ('sheer_id.verify.dl', 'Verify Driver license through Sheer Id');
INSERT INTO user_permission (permission, description) VALUES ('sheer_id.verify.read', 'View Sheer Id verification lookup historical data');

-- super user group gets all new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('sheer_id.verify.dl', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('sheer_id.verify.read', (select id from user_group where machine_name='all'));
