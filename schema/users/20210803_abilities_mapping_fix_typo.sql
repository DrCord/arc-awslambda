UPDATE user_ability_permission_join SET permission = 'users.user.write' WHERE permission = 'users.users.write';
DELETE FROM user_ability_permission_join WHERE permission = 'telemetry.version.read';