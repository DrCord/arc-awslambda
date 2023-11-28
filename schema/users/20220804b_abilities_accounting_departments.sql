-- USE exsiting 'Fleets Admin' user_ability
-- relate permissions to  ability
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES 
  
  ('fleets.accounting_department_code.create', (select id from user_ability where ability='Fleets Admin')),
  ('fleets.accounting_department_code.delete', (select id from user_ability where ability='Fleets Admin')),
  ('fleets.accounting_department_code.update', (select id from user_ability where ability='Fleets Admin'));

-- add permissions to super admin ability
INSERT INTO user_ability_permission_join (permission, ability_id) VALUES 
  ('fleets.accounting_department_code.create', (select id from user_ability where constant='SUPER_ADMIN')),
  ('fleets.accounting_department_code.delete', (select id from user_ability where constant='SUPER_ADMIN')),
  ('fleets.accounting_department_code.update', (select id from user_ability where constant='SUPER_ADMIN'));
