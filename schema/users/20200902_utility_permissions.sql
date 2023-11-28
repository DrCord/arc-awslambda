-- insert notes permissions
INSERT INTO user_permission (permission, description) VALUES ('odoo.label.print', 'Print label via request to printer managed by Odoo.');

-- super user group gets all new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('odoo.label.print', (select id from user_group where machine_name='all'));
