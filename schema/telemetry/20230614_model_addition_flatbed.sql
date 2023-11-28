BEGIN;
-- new flatbed model
INSERT INTO vehicle_model (model_name, letter_code, platform_id, description) VALUES ('Flatbed', 'B', (select id from vehicle_platform where platform_name='FUV 1.0'), 'Flatbed similar to pickup truck.');
-- flatbed model release info
-- Flatbed
INSERT INTO vehicle_model_release (model_id, description) VALUES ((select id from vehicle_model where model_name='Flatbed'), 'Flatbed: Original Manufactured');
INSERT INTO vehicle_model_release (model_id, description) VALUES ((select id from vehicle_model where model_name='Flatbed'), 'Flatbed: Discoboard');
INSERT INTO vehicle_model_release (model_id, description) VALUES ((select id from vehicle_model where model_name='Flatbed'), 'Flatbed: KERS w/o DISCO Board');
INSERT INTO vehicle_model_release (model_id, description) VALUES ((select id from vehicle_model where model_name='Flatbed'), 'Flatbed: KERS Sensor');
-- parts info
-- Flatbed
-- Flatbed: Original Manufactured
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Original Manufactured'), 'BMS', '001052');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Original Manufactured'), 'Charger', '001940');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Original Manufactured'), 'Comm', '004280');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Original Manufactured'), 'Display', '004280');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Original Manufactured'), 'EPSU', '001960');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Original Manufactured'), 'H Bridge', '003223');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Original Manufactured'), 'Inverters', '004085');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Original Manufactured'), 'IO Front', '003225');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Original Manufactured'), 'IO Rear', '003224');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Original Manufactured'), 'LV', '004313');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Original Manufactured'), 'VCU', '003222');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Original Manufactured'), 'KERS Sensor', '001325');
-- Flatbed: Discoboard
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Discoboard'), 'BMS', '001052');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Discoboard'), 'Charger', '001940');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Discoboard'), 'Comm', '004280');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Discoboard'), 'Display', '004280');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Discoboard'), 'EPSU', '001960');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Discoboard'), 'H Bridge', '003223');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Discoboard'), 'Inverters', '004085');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Discoboard'), 'IO Front', '003225');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Discoboard'), 'IO Rear', '003224');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Discoboard'), 'LV', '004313');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Discoboard'), 'VCU', '003222');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: Discoboard'), 'KERS Sensor', '001325');
-- Flatbed: KERS w/o DISCO Board
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS w/o DISCO Board'), 'BMS', '001052');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS w/o DISCO Board'), 'Charger', '001940');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS w/o DISCO Board'), 'Comm', '004280');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS w/o DISCO Board'), 'Display', '004280');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS w/o DISCO Board'), 'EPSU', '001960');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS w/o DISCO Board'), 'H Bridge', '003223');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS w/o DISCO Board'), 'Inverter - Left', '004085');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS w/o DISCO Board'), 'Inverter - Right', '004085');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS w/o DISCO Board'), 'IO Front', '003225');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS w/o DISCO Board'), 'IO Rear', '003224');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS w/o DISCO Board'), 'LV', '004313');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS w/o DISCO Board'), 'VCU', '003222');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS w/o DISCO Board'), 'KERS Sensor', '001325');
-- Flatbed: KERS Sensor
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS Sensor'), 'BMS', '001052');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS Sensor'), 'Charger', '001940');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS Sensor'), 'Comm', '004280');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS Sensor'), 'Display', '004280');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS Sensor'), 'EPSU', '001960');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS Sensor'), 'H Bridge', '003223');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS Sensor'), 'Inverter - Left', '004085');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS Sensor'), 'Inverter - Right', '004085');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS Sensor'), 'IO Front', '003225');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS Sensor'), 'IO Rear', '003224');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS Sensor'), 'LV', '004313');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS Sensor'), 'VCU', '003222');
INSERT INTO vehicle_model_parts (model_release_id, part_type, part_number) VALUES ((select model_release_id from vehicle_model_release where description='Flatbed: KERS Sensor'), 'KERS Sensor', '001412');
COMMIT;