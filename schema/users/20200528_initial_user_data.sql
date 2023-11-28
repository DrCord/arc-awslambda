-- truncate and reset counter for related tables
TRUNCATE user_profile, user_group_join RESTART IDENTITY CASCADE;

-- insert all users and their groups

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('0623209d-d844-4d9f-a567-ddaecccc0f1f', 'Jackie Brewer', '+15419532072', 'jacklynb@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('0623209d-d844-4d9f-a567-ddaecccc0f1f', (select id from user_group where machine_name='delivery'));
INSERT INTO user_group_join (username, group_id) 
  VALUES ('0623209d-d844-4d9f-a567-ddaecccc0f1f', (select id from user_group where machine_name='support'));

-- repeat
-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('067a1168-a490-49b4-83fe-1bd552016670', 'Matthew Buss', '+15038585017', 'matthewb@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('067a1168-a490-49b4-83fe-1bd552016670', (select id from user_group where machine_name='all'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('0a5b82cd-8682-4a92-9f11-11fdb4554313', 'Sam Fittipaldi', '+15415207931', 'samf@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('0a5b82cd-8682-4a92-9f11-11fdb4554313', (select id from user_group where machine_name='support'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('0aa7ef40-6303-4355-b82e-b16e79b4e35c', 'Michael Biron', '+13108833959', 'michaelb@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('0aa7ef40-6303-4355-b82e-b16e79b4e35c', (select id from user_group where machine_name='provision'));
INSERT INTO user_group_join (username, group_id) 
  VALUES ('0aa7ef40-6303-4355-b82e-b16e79b4e35c', (select id from user_group where machine_name='service'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('2ddcd953-b222-4465-bcab-81f7efaae0f2', 'Jacob Dill', '+15417317342', 'jacobd@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('2ddcd953-b222-4465-bcab-81f7efaae0f2', (select id from user_group where machine_name='provision'));
INSERT INTO user_group_join (username, group_id) 
  VALUES ('2ddcd953-b222-4465-bcab-81f7efaae0f2', (select id from user_group where machine_name='service'));


-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('3a56e612-9bab-4549-b41f-ab983ef265e0', 'Wesley Tan', '+15415790544', 'wesleyt@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('3a56e612-9bab-4549-b41f-ab983ef265e0', (select id from user_group where machine_name='all'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('3a93e818-7983-4a91-83fc-80dc7dd1e201', 'Gerrit Hurenkamp', '+15593211694', 'gerrith@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('3a93e818-7983-4a91-83fc-80dc7dd1e201', (select id from user_group where machine_name='all'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('3bcd5498-b64f-43ae-aae0-190748056cc6', 'Raymond', '+15035022385', 'raymonds@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('3bcd5498-b64f-43ae-aae0-190748056cc6', (select id from user_group where machine_name='quality'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('574808bd-edc9-47e7-911a-18eeef5bc958', 'Joe Morgan', '+14582101342', 'joe@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('574808bd-edc9-47e7-911a-18eeef5bc958', (select id from user_group where machine_name='support'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('59b298f2-b73c-4b08-ad36-4ac24ec45745', 'jasonw', '+12069104810', 'jasonw@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('59b298f2-b73c-4b08-ad36-4ac24ec45745', (select id from user_group where machine_name='provision'));
INSERT INTO user_group_join (username, group_id) 
  VALUES ('59b298f2-b73c-4b08-ad36-4ac24ec45745', (select id from user_group where machine_name='service'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('62bab1e8-96bb-442a-98b7-bd2475a4cad8', 'Brian Perry', '+16037628750', 'brianp@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('62bab1e8-96bb-442a-98b7-bd2475a4cad8', (select id from user_group where machine_name='quality'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('64205ac4-4b73-4624-94ce-f4d0093154a2', 'Brandon Carrillo', '+15415172346', 'brandonc@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('64205ac4-4b73-4624-94ce-f4d0093154a2', (select id from user_group where machine_name='provision'));
INSERT INTO user_group_join (username, group_id) 
  VALUES ('64205ac4-4b73-4624-94ce-f4d0093154a2', (select id from user_group where machine_name='service'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('7c48694d-9e12-491f-9b07-64eec50752e9', 'Eric Fritz', '+15416543167', 'fritz@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('7c48694d-9e12-491f-9b07-64eec50752e9', (select id from user_group where machine_name='support'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('8d802465-dad1-4501-92e1-920348cd81ee', 'Matthew Maynard', '+19135227439', 'mattm@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('8d802465-dad1-4501-92e1-920348cd81ee', (select id from user_group where machine_name='delivery'));
INSERT INTO user_group_join (username, group_id) 
  VALUES ('8d802465-dad1-4501-92e1-920348cd81ee', (select id from user_group where machine_name='quality'));
INSERT INTO user_group_join (username, group_id) 
  VALUES ('8d802465-dad1-4501-92e1-920348cd81ee', (select id from user_group where machine_name='support'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('8ffcb751-da21-4f71-91a9-a338e16cd6db', 'Cord Slatton', '+15413577252', 'cords@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('8ffcb751-da21-4f71-91a9-a338e16cd6db', (select id from user_group where machine_name='all'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('9cd63c62-d538-4421-8482-e58a7bcf2dd5', 'Chris Ham', '+17025720031', 'chrish@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('9cd63c62-d538-4421-8482-e58a7bcf2dd5', (select id from user_group where machine_name='all'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('a90cbc0b-fcdd-4333-9d69-8ab7d805aeaf', 'Jove', '+15418526396', 'jove@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('a90cbc0b-fcdd-4333-9d69-8ab7d805aeaf', (select id from user_group where machine_name='quality'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('b375bb7f-68d3-4853-bb18-c3d6316636d3', 'Chris Coleman', '+15415436087', 'chris.coleman@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('b375bb7f-68d3-4853-bb18-c3d6316636d3', (select id from user_group where machine_name='quality'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('b7e9d54f-8ffd-44db-9786-dd0840585de7', 'Keith Anderson', '+15415153689', 'keitha@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('b7e9d54f-8ffd-44db-9786-dd0840585de7', (select id from user_group where machine_name='all'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('ba75b2ac-4ce2-4263-a1bb-664634e4c16c', 'Ray Nichols', '+15416065536', 'rayn@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('ba75b2ac-4ce2-4263-a1bb-664634e4c16c', (select id from user_group where machine_name='delivery'));
INSERT INTO user_group_join (username, group_id) 
  VALUES ('ba75b2ac-4ce2-4263-a1bb-664634e4c16c', (select id from user_group where machine_name='support'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('c46aeb3f-33aa-4e57-9f97-cbc1eadc4176', 'Brandon McConnell', '+15417338297', 'brandonm@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('c46aeb3f-33aa-4e57-9f97-cbc1eadc4176', (select id from user_group where machine_name='provision'));
INSERT INTO user_group_join (username, group_id) 
  VALUES ('c46aeb3f-33aa-4e57-9f97-cbc1eadc4176', (select id from user_group where machine_name='service'));

-- insert user & groups
INSERT INTO user_profile (username, display_name, phone, email) 
  VALUES ('d7114c0e-bd16-42f4-9fe0-96832ebc3042', 'Travis Travelstead', '+19713319604', 'travis@arcimoto.com');
INSERT INTO user_group_join (username, group_id) 
  VALUES ('d7114c0e-bd16-42f4-9fe0-96832ebc3042', (select id from user_group where machine_name='provision'));
