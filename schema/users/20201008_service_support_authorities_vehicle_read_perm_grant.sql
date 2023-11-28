INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.vehicle.read', (select id from user_group where machine_name='service'));

INSERT INTO user_permission_group_join (permission, group_id) VALUES ('authorities.vehicle.read', (select id from user_group where machine_name='support'));