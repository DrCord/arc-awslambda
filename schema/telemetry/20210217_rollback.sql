ALTER TABLE vehicle DROP COLUMN model_release_id;
ALTER TABLE vehicle RENAME COLUMN created TO created_at;

ALTER TABLE vehicle DROP CONSTRAINT model_release_id;

ALTER TABLE vehicle_parts_installed DROP CONSTRAINT vin;

ALTER TABLE vehicle_parts_installed DROP CONSTRAINT part_number;

ALTER TABLE vehicle_firmware_installed DROP CONSTRAINT vin;

ALTER TABLE vehicle_firmware_installed DROP CONSTRAINT firmware_release_id;

ALTER TABLE vehicle_model_release DROP CONSTRAINT model_release_id;

ALTER TABLE vehicle_model_parts DROP CONSTRAINT firmware_min_release;

ALTER TABLE vehicle_model_parts DROP CONSTRAINT firmware_max_release;

DROP TABLE vehicle_parts_installed;

DROP TABLE vehicle_firmware_installed;

DROP TABLE vehicle_model_release;

DROP TABLE vehicle_model_parts;

DROP TABLE firmware_release;


