ALTER TABLE user_permission DROP CONSTRAINT user_permission_pkey;
ALTER TABLE user_permission ADD CONSTRAINT user_permission_pkey PRIMARY KEY (permission, resource);

ALTER TABLE user_profile 
    ADD COLUMN display_name text default NULL,
    ADD COLUMN avatar bytea default NULL;

CREATE TABLE user_preferences (
    preference VARCHAR(200) PRIMARY KEY,
    description text not NULL
);

CREATE TABLE user_profile_join_user_preferences (
    preference VARCHAR(200) not NULL,
    username varchar(200) not NULL,
    PRIMARY KEY (preference, username)
);

CREATE TABLE users_join_vehicle_group (
    username varchar(200) not NULL,
    vehicle_group integer not NULL,
    PRIMARY KEY (username, vehicle_group)
);
