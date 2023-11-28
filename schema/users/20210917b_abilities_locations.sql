-- create new ability
INSERT INTO user_ability (ability, description, constant) VALUES ('Locations Admin', 'All location functionality', 'LOCATIONS_ADMIN');
-- relate permissions to new ability
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES 
  ('locations.update', (select id from user_ability where ability='Locations Admin')),
  ('locations.delete', (select id from user_ability where ability='Locations Admin'));

-- add permissions to super admin ability
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES 
  ('locations.update', (select id from user_ability where constant='SUPER_ADMIN')),
  ('locations.delete', (select id from user_ability where constant='SUPER_ADMIN'));
