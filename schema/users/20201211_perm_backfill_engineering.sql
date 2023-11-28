-- insert arcimoto group association remove permission
INSERT INTO user_permission (permission, description) VALUES ('telemetry.backfill.engineering', 'Initiate telemetry data backfill request');

-- super user group gets all new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('telemetry.backfill.engineering', (select id from user_group where machine_name='all'));

-- service group needs this new permission
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('telemetry.backfill.engineering', (select id from user_group where machine_name='service'));
