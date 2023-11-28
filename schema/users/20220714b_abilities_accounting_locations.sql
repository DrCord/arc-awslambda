-- USE exsiting 'Locations Admin' user_ability
-- relate permissions to  ability
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES 
  
  ('locations.code.create', (select id from user_ability where ability='Locations Admin')),
  ('locations.code.delete', (select id from user_ability where ability='Locations Admin')),
  ('locations.code.update', (select id from user_ability where ability='Locations Admin'));

-- add permissions to super admin ability
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES 
  ('locations.code.create', (select id from user_ability where constant='SUPER_ADMIN')),
  ('locations.code.delete', (select id from user_ability where constant='SUPER_ADMIN')),
  ('locations.code.update', (select id from user_ability where constant='SUPER_ADMIN'));
