-- insert notes permissions
INSERT INTO user_permission (permission, description) VALUES ('notes.note.delete', 'Delete note');

-- super user group gets all new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('notes.note.delete', (select id from user_group where machine_name='all'));
