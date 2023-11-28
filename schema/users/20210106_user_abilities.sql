ALTER TABLE user_permission
ALTER COLUMN resource TYPE VARCHAR(200);

CREATE TABLE user_ability (
    id serial PRIMARY KEY,
    ability VARCHAR(200) not NULL,
    description text not NULL
);

CREATE TABLE user_ability_permission_join (
    permission VARCHAR(200) not NULL,
    permission_resource VARCHAR(200) not NULL default '*',
    ability_id integer not NULL,
    PRIMARY KEY (permission, permission_resource, ability_id)
);

-- allow users access to tables
GRANT SELECT ON user_ability TO user_permission_check;
GRANT SELECT ON user_ability_permission_join TO user_permission_check;
GRANT USAGE, SELECT ON SEQUENCE user_ability_id_seq TO user_permission_check;

GRANT SELECT ON user_ability TO users_public;
GRANT SELECT ON user_ability_permission_join TO users_public;
GRANT USAGE, SELECT ON SEQUENCE user_ability_id_seq TO users_public;

GRANT SELECT, INSERT, UPDATE, DELETE ON user_ability TO users_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON user_ability_permission_join TO users_administration;
GRANT USAGE, SELECT ON SEQUENCE user_ability_id_seq TO users_administration;

-- insert permissions
INSERT INTO user_permission (permission, description) VALUES ('users.abilities.create', 'Create ability to permission mapping');
INSERT INTO user_permission (permission, description) VALUES ('users.abilities.read', 'Read ability to permission mappings outside of context of own user');
INSERT INTO user_permission (permission, description) VALUES ('users.abilities.update', 'Edit ability to permission mapping');
INSERT INTO user_permission (permission, description) VALUES ('users.abilities.delete', 'Delete ability to permission mapping');

-- super user group gets all new permissions
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.abilities.create', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.abilities.read', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.abilities.update', (select id from user_group where machine_name='all'));
INSERT INTO user_permission_group_join (permission, group_id) VALUES ('users.abilities.delete', (select id from user_group where machine_name='all'));