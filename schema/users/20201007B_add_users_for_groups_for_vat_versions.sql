-- add groups for Raymond S
INSERT INTO user_group_join (username, group_id) 
  VALUES ('3bcd5498-b64f-43ae-aae0-190748056cc6', (select id from user_group where machine_name='service'));

INSERT INTO user_group_join (username, group_id) 
  VALUES ('3bcd5498-b64f-43ae-aae0-190748056cc6', (select id from user_group where machine_name='recall_admin'));