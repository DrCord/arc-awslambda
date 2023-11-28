  -- insert permissions
INSERT INTO user_permission (permission, description) VALUES 
   ('fleets.accounting_department_code.create', 'Create accounting department code records'),
   ('fleets.accounting_department_code.delete', 'Delete accounting department code records'),
   ('fleets.accounting_department_code.update', 'Update accounting department code records')
  ;

-- super user group gets all new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES 
  ('fleets.accounting_department_code.create', (select id from user_group where machine_name='all')),
  ('fleets.accounting_department_code.delete', (select id from user_group where machine_name='all')),
  ('fleets.accounting_department_code.update', (select id from user_group where machine_name='all'))
  ;

  INSERT INTO user_permission_group_join (permission, group_id) VALUES 
  ('fleets.accounting_department_code.create', (select id from user_group where machine_name='fleets_admin')),
  ('fleets.accounting_department_code.delete', (select id from user_group where machine_name='fleets_admin')),
  ('fleets.accounting_department_code.update', (select id from user_group where machine_name='fleets_admin'))
  ;
