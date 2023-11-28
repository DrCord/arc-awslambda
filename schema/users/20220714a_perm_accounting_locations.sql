  -- insert permissions
INSERT INTO user_permission (permission, description) VALUES 
   ('locations.code.create', 'Create accounting location code records'),
   ('locations.code.delete', 'Delete accounting location code records'),
   ('locations.code.update', 'Update accounting location code records')
  ;

-- super user group gets all new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES 
  ('locations.code.create', (select id from user_group where machine_name='all')),
  ('locations.code.delete', (select id from user_group where machine_name='all')),
  ('locations.code.update', (select id from user_group where machine_name='all'))
  ;
