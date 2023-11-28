-- insert permissions
INSERT INTO user_permission (permission, description) VALUES ('managed_session.session.start', 'Initiate managed session for a vehicle');
INSERT INTO user_permission (permission, description) VALUES ('managed_session.session.end', 'End any managed sessions for a vehicle');
INSERT INTO user_permission (permission, description) VALUES ('managed_session.session.read', 'Get managed session(s) data');

-- super user group gets all new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('managed_session.session.start', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('managed_session.session.end', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('managed_session.session.read', (select id from user_group where machine_name='all'));
