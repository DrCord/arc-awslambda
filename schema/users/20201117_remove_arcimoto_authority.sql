-- insert arcimoto group association remove permission
INSERT INTO user_permission (permission, description) VALUES ('authorities.vehicle.unsign_arcimoto', 'Remove Arcimoto fleet/vehicle group association');

-- super user group gets all new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.vehicle.unsign_arcimoto', (select id from user_group where machine_name='all'));

-- provision group needs this new permission
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.vehicle.unsign_arcimoto', (select id from user_group where machine_name='provision'));
