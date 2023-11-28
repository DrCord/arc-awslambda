-- Create a DB role for main.public role
-- NOTE: Password for this role will be NULL (preventing login) until manually set
CREATE ROLE main_public WITH LOGIN;
GRANT SELECT ON meta TO main_public;
GRANT SELECT ON notes TO main_public;
GRANT SELECT ON notes_tags TO main_public;
GRANT SELECT ON notes_tags_join TO main_public;
GRANT SELECT ON recall_remedies TO main_public;
GRANT SELECT ON recalls TO main_public;
GRANT SELECT ON telemetry_definition TO main_public;
GRANT SELECT ON telemetry_points TO main_public;
GRANT SELECT ON tsb TO main_public;
GRANT SELECT ON tsb_remedies TO main_public;
GRANT SELECT ON user_profile_join_user_preferences TO main_public;
GRANT SELECT ON vehicle TO main_public;
GRANT SELECT ON vehicle_group TO main_public;
GRANT SELECT ON vehicle_join_vehicle_group TO main_public;
GRANT SELECT ON vehicle_meta TO main_public;
GRANT SELECT ON vehicle_recalls TO main_public;
GRANT SELECT ON vehicle_tsb TO main_public;

-- Create a DB role for users.administration role
-- NOTE: Password for this role will be NULL (preventing login) until manually set
CREATE ROLE main_administration WITH LOGIN;
GRANT SELECT, INSERT, UPDATE, DELETE ON meta TO main_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON notes TO main_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON notes_tags TO main_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON notes_tags_join TO main_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON recall_remedies TO main_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON recalls TO main_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON telemetry_definition TO main_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON telemetry_points TO main_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON tsb TO main_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON tsb_remedies TO main_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON user_profile_join_user_preferences TO main_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON vehicle TO main_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON vehicle_group TO main_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON vehicle_join_vehicle_group TO main_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON vehicle_meta TO main_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON vehicle_recalls TO main_administration;
GRANT SELECT, INSERT, UPDATE, DELETE ON vehicle_tsb TO main_administration;