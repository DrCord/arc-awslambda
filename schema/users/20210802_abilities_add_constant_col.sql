ALTER TABLE user_ability ADD COLUMN constant varchar(50) default NULL;

UPDATE user_ability SET constant = 'VEHICLE_PROVISION' WHERE id = 1;
UPDATE user_ability SET constant = 'AUTHORITY_CREATE' WHERE id = 2;
UPDATE user_ability SET constant = 'FLEET_ADMIN' WHERE id = 3;
UPDATE user_ability SET constant = 'VEHICLE_DELIVER' WHERE id = 4;
UPDATE user_ability SET constant = 'VEHICLE_QUALITY' WHERE id = 5;
UPDATE user_ability SET constant = 'AUTHORITY_ADMIN' WHERE id = 6;
UPDATE user_ability SET constant = 'MANAGED_SESSION_ADMIN' WHERE id = 7;
UPDATE user_ability SET constant = 'RECALL_ADMIN' WHERE id = 8;
UPDATE user_ability SET constant = 'VEHICLE_BACKFILL_TELEMETRY' WHERE id = 9;
UPDATE user_ability SET constant = 'VEHICLE_READ' WHERE id = 10;
UPDATE user_ability SET constant = 'VEHICLE_FIRMWARE_READ' WHERE id = 11;
UPDATE user_ability SET constant = 'VEHICLE_FIRMWARE_WRITE' WHERE id = 12;
UPDATE user_ability SET constant = 'FIRMWARE_ADMIN' WHERE id = 13;
UPDATE user_ability SET constant = 'VEHICLE_GPS_RECORD_READ' WHERE id = 14;
UPDATE user_ability SET constant = 'VEHICLE_GPS_RECORD_WRITE' WHERE id = 15;
UPDATE user_ability SET constant = 'VEHICLE_TELMETRY_CONFIG_WRITE' WHERE id = 16;
UPDATE user_ability SET constant = 'VEHICLE_TELMETRY_CONFIG_READ' WHERE id = 17;
UPDATE user_ability SET constant = 'VEHICLE_MANUFACTURING_CONFIG_READ' WHERE id = 18;
UPDATE user_ability SET constant = 'VEHICLE_MANUFACTURING_CONFIG_WRITE' WHERE id = 19;
UPDATE user_ability SET constant = 'VEHICLE_TOKEN_SIGN' WHERE id = 20;
UPDATE user_ability SET constant = 'VEHICLE_MAIN_ADMIN' WHERE id = 21;
UPDATE user_ability SET constant = 'VEHICLE_FACTORY_PIN_READ' WHERE id = 22;
UPDATE user_ability SET constant = 'VEHICLE_NOTES_READ' WHERE id = 23;
UPDATE user_ability SET constant = 'VEHICLE_NOTES_CREATE' WHERE id = 24;
UPDATE user_ability SET constant = 'USER_READ' WHERE id = 25;
UPDATE user_ability SET constant = 'USER_ADMIN' WHERE id = 26;
UPDATE user_ability SET constant = 'USER_PROFILE_WRITE' WHERE id = 27;
UPDATE user_ability SET constant = 'USER_CREATE' WHERE id = 28;
UPDATE user_ability SET constant = 'USER_ENABLED_WRITE' WHERE id = 29;
UPDATE user_ability SET constant = 'USER_PERMISSION_GROUPS_READ' WHERE id = 30;
UPDATE user_ability SET constant = 'ODOO_LABEL_PRINT' WHERE id = 31;
UPDATE user_ability SET constant = 'PERMISSION_GROUP_CREATE' WHERE id = 32;
UPDATE user_ability SET constant = 'PERMISSION_GROUP_WRITE' WHERE id = 33;
UPDATE user_ability SET constant = 'PERMISSIONS_READ' WHERE id = 34;
UPDATE user_ability SET constant = 'PERMISSION_GROUP_ADD_PERMISSION' WHERE id = 35;
UPDATE user_ability SET constant = 'PERMISSION_GROUP_REMOVE_PERMISSION' WHERE id = 36;
UPDATE user_ability SET constant = 'ABILITIES_READ' WHERE id = 37;
UPDATE user_ability SET constant = 'ABILITIES_CREATE' WHERE id = 38;
UPDATE user_ability SET constant = 'PERMISSION_ADMIN' WHERE id = 39;
UPDATE user_ability SET constant = 'TELEMETRY_ADMIN' WHERE id = 40;
UPDATE user_ability SET constant = 'RECALLS_SERVICE' WHERE id = 41;
UPDATE user_ability SET constant = 'VEHICLE_AUTHORITIES_READ' WHERE id = 42;
UPDATE user_ability SET constant = 'SUPER_ADMIN' WHERE id = 43;
UPDATE user_ability SET constant = 'AUTHORITIES_LIST' WHERE id = 44;
UPDATE user_ability SET constant = 'RECALLS_READ' WHERE id = 45;
UPDATE user_ability SET constant = 'FLEETS_GROUP_READ' WHERE id = 46;