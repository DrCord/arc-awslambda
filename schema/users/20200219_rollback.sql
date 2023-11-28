ALTER TABLE user_permission DROP CONSTRAINT user_permission_pkey;
ALTER TABLE user_permission ADD CONSTRAINT user_permission_pkey PRIMARY KEY (permission);

ALTER TABLE user_profile DROP COLUMN display_name;
ALTER TABLE user_profile DROP COLUMN avatar;

DROP TABLE user_preferences;
DROP TABLE user_profile_preferences_join;
DROP TABLE users_join_vehicle_group;