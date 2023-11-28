# Resource Bundle: Users

The User resource bundle implements all aspect of the per-user model, including access control, preferences, profile and other user-centric data.

## References

### Primary Objects

- User: The core resource object in this bundle.
- Permission: Determines policy access limits.
- Group: Permissions are linked to groups, and membership in a group determines the users' permission.

### Schema

- schema/telemetry/20200207_add_user_permissions.sql
  - Initial tables
- schema/telemetry/20200219_modify_user_permissions.sql
  - Fixed incorrect primary key in user_permission table
  - Added profile and preferences
  - Added vehicle permission control table
- schema/telemetry/20200225_add_missing_preference_join_column.sql
  - Added preference value storage
- schema/telemetry/20200316_user_profile_additions.sql
  - Add email and phone to profile

### Roles

List all roles defined by this bundle. Lambdas will assume these roles depending on what access they need to function.

#### users.administration

##### Attached Policy

- AWSLambdaVPCAccessExecutionRole (Default AWS)
- cognito.admin-pool.ArcimotoUsers-Dev
- sqs.send.message-broker
- secrets.read.users_administration_db_dev

##### Policy Details

- read access to DB tables:
  - user_group
  - user_profile
  - user_group_join
  - user_permission
  - user_permission_group_join
  - user_preferences
  - user_profile_join_user_preferences
- write access to DB tables:
  - user_group
  - user_profile
  - user_group_join
  - user_permission
  - user_permission_group_join
  - user_preferences
  - user_profile_join_user_preferences
- Create user records in cognito pool
- Send notifications

#### users.public

##### Attached Policy

- AWSLambdaVPCAccessExcecutionRole (Default AWS)
- sqs.send.message-broker
- secrets.read.user_public_db_dev

##### Policy Details

- read access to DB tables:
  - user_group
  - user_profile
  - user_group_join
  - user_permission
  - user_permission_group_join
  - user_preferences
  - user_profile_join_user_preferences
- write access to DB tables
  - user_preferences [restricted to self]
  - user_profile [restricted to self]

### Dependencies

This bundle is used extensively by the *arcimoto* core package in order to provide consistent authorization controls for the current user.

## Functions

### Administration Functions

- users_create_user
  - PERM: users.user.create
  - API: POST /users/create
  - Creates a Cognito user with the specified name, email and phone number. Creates user records with Cognito UUID as the username.
- users_disable_user
  - PERM: users.user.disable
  - API:
- users_enable_user
  - PERM: users.user.enable
  - API:
- users_group_create
  - PERM: users.group.create
  - API: POST /groups/create
- users_add_user_to_group
  - PERM: users.group.write
  - API: PUT /groups/{group}/users/{username}
- users_remove_user_from_group
  - PERM: users.group.write
  - API: DELETE /groups/{group}/users/{username}
- users_group_delete
  - PERM: users.group.delete
  - API: DELETE /groups/{group}
- users_add_permission_to_group
  - PERM: users.group.add-permission
  - API: PUT /groups/{group}/permissions/{permission}
- users_remove_permission_from_group
  - PERM: users.group.remove-permission
  - API: DELETE /groups/{group}/permissions/{permission}

### Public Access Functions

- users_group_get
  - PERM: users.group.read
  - API: GET /groups/{group}
- users_profile_get
  - PERM: users.user-profile.read
  - API: GET /users/{username}/profile
- users_profile_update
  - PERM: users.user-profile.write
  - API: POST /users/{username}/profile
- users_preferences_get
  - PERM: users.user-prefs.read
  - API:
- users_preferences_set
  - PERM: users.user-prefs.write
  - API: 
- users_user_get
  - PERM: users.user.read
  - API: GET /users/{username}
  - Fetches all info about a user (including cognito status, profile, prefs and perms)

## Implementation Notes (For Toddlers)

rrfdzaxfdeyyyyttttttttyyy
juy7y76tew5wsaww5r654q 1`2 23q2221qqqqqerree
