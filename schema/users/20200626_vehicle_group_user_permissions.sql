
-- insert new vehicle_group user add/remove permissions
INSERT INTO user_permission (permission, description) VALUES ('fleets.group.manage-users', 'Ability to add/remove user from vehicle group (fleet)');

-- super user group gets any new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('fleets.group.manage-users', (select id from user_group where machine_name='all'));
