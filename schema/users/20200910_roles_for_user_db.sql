-- Create a DB role for users.public role
-- NOTE: Password for this role will be NULL (preventing login) until manually set
CREATE ROLE users_public WITH LOGIN;
GRANT SELECT ON user_group TO users_public;
GRANT USAGE, SELECT ON SEQUENCE user_group_id_seq TO users_public;
GRANT SELECT ON user_permission TO users_public;
GRANT SELECT, UPDATE ON user_profile TO users_public;
GRANT SELECT ON user_group_join TO users_public;
GRANT SELECT ON user_permission_group_join TO users_public;
GRANT SELECT, INSERT, UPDATE, DELETE ON user_preferences TO users_public;
GRANT SELECT, INSERT, UPDATE, DELETE ON user_profile_join_user_preferences TO users_public;


-- Create a DB role for users.administration role
-- NOTE: Password for this role will be NULL (preventing login) until manually set
CREATE ROLE users_administration WITH LOGIN;
GRANT SELECT, INSERT, UPDATE, DELETE ON user_group TO users_administration;
GRANT USAGE, SELECT ON SEQUENCE user_group_id_seq TO users_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON user_permission TO users_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON user_profile TO users_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON user_group_join TO users_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON user_permission_group_join TO users_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON user_preferences TO users_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON user_profile_join_user_preferences TO users_administration;