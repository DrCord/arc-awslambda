BEGIN;
ALTER TABLE firmware_versions drop constraint firmware_versions_pkey;
ALTER TABLE firmware_versions ADD CONSTRAINT firmware_versions_pkey PRIMARY KEY (firmware_component, hash);
INSERT INTO firmware_versions (firmware_component, hash) VALUES ('004280 Comm Bootloader', 'e736bac9216d010621a38436a65582cc00a3231a');
COMMIT;