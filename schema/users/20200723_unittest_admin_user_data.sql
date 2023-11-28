-- insert unittest user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('47a728a9-db7c-4294-9ad2-87d293135025', 'Unit Test Admin', '', 'unittest_admin@arcimoto.com');

  INSERT INTO user_group_join (username, group_id) 
  VALUES ('47a728a9-db7c-4294-9ad2-87d293135025', (select id from user_group where machine_name='all'));
