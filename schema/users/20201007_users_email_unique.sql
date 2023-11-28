CREATE UNIQUE INDEX CONCURRENTLY user_profile_email ON user_profile (email);

ALTER TABLE user_profile ADD CONSTRAINT unique_email UNIQUE USING INDEX user_profile_email;