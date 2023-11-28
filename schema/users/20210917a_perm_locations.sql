-- insert permissions
INSERT INTO user_permission (permission, description) VALUES 
  ('locations.update', 'Update location records'),
  ('locations.delete', 'Delete location records');

-- super user group gets all new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES 
  ('locations.update', (select id from user_group where machine_name='all')),
  ('locations.delete', (select id from user_group where machine_name='all'));
