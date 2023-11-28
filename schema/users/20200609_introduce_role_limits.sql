-- Create a role for global/public permission lookups
-- NOTE: Password for this role will be NULL (preventing login) until manually set
CREATE ROLE user_permission_check WITH LOGIN;
-- User group and permission lookup
GRANT SELECT ON user_group TO user_permission_check;
GRANT SELECT ON user_permission TO user_permission_check;