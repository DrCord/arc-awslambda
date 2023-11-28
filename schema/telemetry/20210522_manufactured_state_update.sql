-- all existing vehicles need to have their model_release_id updated to reflect their manufactured state
-- NOTES:
----  VIN for "(NOT) IN" needs per ENV adjustment due to prefix
----  SUBSTRING start needs adjustment due to prefix: DEV: 9, STAGING: 11, PROD: 5

-- make sure no vehicles are set to NULL
UPDATE vehicle SET model_release_id = 1;

-- FUV
-- don't worry about pre-discoboard FUV, these will be everything left after the rest are picked out
-- discoboard/pre-KERS Sensor switch
UPDATE vehicle SET model_release_id = (select model_release_id from vehicle_model_release where description = 'FUV: Discoboard') WHERE SUBSTRING (vin, 5, 1) = (select letter_code from vehicle_model where model_name = 'FUV') AND vin NOT IN (select vin from vehicle where created >= (select created from vehicle where vin = '7F7ADR311MER00019')) AND vin IN (select vin from vehicle_parts_installed where part_type = 'Comm' and part_number = '004280');
-- post KERS Sensor switch
UPDATE vehicle SET model_release_id = (select model_release_id from vehicle_model_release where description = 'FUV: KERS Sensor') WHERE SUBSTRING (vin, 5, 1) = (select letter_code from vehicle_model where model_name = 'FUV') AND vin IN (select vin from vehicle where created >= (select created from vehicle where vin = '7F7ADR311MER00019'));

-- Camera Car
-- pre discoboard
UPDATE vehicle SET model_release_id = (select model_release_id from vehicle_model_release where description = 'Camera Car: Original Manufactured') WHERE SUBSTRING (vin, 5, 1) = (select letter_code from vehicle_model where model_name = 'Camera Car') AND vin NOT IN (select vin from vehicle where created >= (select created from vehicle where vin = '7F7ADR311MER00019')) AND vin IN (select vin from vehicle_parts_installed where part_type = 'Comm' and part_number != '004280');
-- discoboard/pre-KERS Sensor switch
UPDATE vehicle SET model_release_id = (select model_release_id from vehicle_model_release where description = 'Camera Car: Discoboard') WHERE SUBSTRING (vin, 5, 1) = (select letter_code from vehicle_model where model_name = 'Camera Car') AND vin NOT IN (select vin from vehicle where created >= (select created from vehicle where vin = '7F7ADR311MER00019')) AND vin IN (select vin from vehicle_parts_installed where part_type = 'Comm' and part_number = '004280');
-- post KERS Sensor switch
UPDATE vehicle SET model_release_id = (select model_release_id from vehicle_model_release where description = 'Camera Car: KERS Sensor') WHERE SUBSTRING (vin, 5, 1) = (select letter_code from vehicle_model where model_name = 'Camera Car') AND vin IN (select vin from vehicle where created >= (select created from vehicle where vin = '7F7ADR311MER00019'));

-- Deliverator
-- pre discoboard
UPDATE vehicle SET model_release_id = (select model_release_id from vehicle_model_release where description = 'Deliverator: Original Manufactured') WHERE SUBSTRING (vin, 5, 1) = (select letter_code from vehicle_model where model_name = 'Deliverator') AND vin NOT IN (select vin from vehicle where created >= (select created from vehicle where vin = '7F7ADR311MER00019')) AND vin IN (select vin from vehicle_parts_installed where part_type = 'Comm' and part_number != '004280');
-- discoboard/pre-KERS Sensor switch
UPDATE vehicle SET model_release_id = (select model_release_id from vehicle_model_release where description = 'Deliverator: Discoboard') WHERE SUBSTRING (vin, 5, 1) = (select letter_code from vehicle_model where model_name = 'Deliverator') AND vin NOT IN (select vin from vehicle where created >= (select created from vehicle where vin = '7F7ADR311MER00019')) AND vin IN (select vin from vehicle_parts_installed where part_type = 'Comm' and part_number = '004280');
-- post KERS Sensor switch
UPDATE vehicle SET model_release_id = (select model_release_id from vehicle_model_release where description = 'Deliverator: KERS Sensor') WHERE SUBSTRING (vin, 5, 1) = (select letter_code from vehicle_model where model_name = 'Deliverator') AND vin IN (select vin from vehicle where created >= (select created from vehicle where vin = '7F7ADR311MER00019'));

-- Rapid Responder
-- pre discoboard
UPDATE vehicle SET model_release_id = (select model_release_id from vehicle_model_release where description = 'Rapid Responder: Original Manufactured') WHERE SUBSTRING (vin, 5, 1) = (select letter_code from vehicle_model where model_name = 'Rapid Responder') AND vin NOT IN (select vin from vehicle where created >= (select created from vehicle where vin = '7F7ADR311MER00019')) AND vin IN (select vin from vehicle_parts_installed where part_type = 'Comm' and part_number != '004280');
-- discoboard/pre-KERS Sensor switch
UPDATE vehicle SET model_release_id = (select model_release_id from vehicle_model_release where description = 'Rapid Responder: Discoboard') WHERE SUBSTRING (vin, 5, 1) = (select letter_code from vehicle_model where model_name = 'Rapid Responder') AND vin NOT IN (select vin from vehicle where created >= (select created from vehicle where vin = '7F7ADR311MER00019')) AND vin IN (select vin from vehicle_parts_installed where part_type = 'Comm' and part_number = '004280');
-- post KERS Sensor switch
UPDATE vehicle SET model_release_id = (select model_release_id from vehicle_model_release where description = 'Rapid Responder: KERS Sensor') WHERE SUBSTRING (vin, 5, 1) = (select letter_code from vehicle_model where model_name = 'Rapid Responder') AND vin IN (select vin from vehicle where created >= (select created from vehicle where vin = '7F7ADR311MER00019'));

-- Responderator
-- pre discoboard
UPDATE vehicle SET model_release_id = (select model_release_id from vehicle_model_release where description = 'Responderator: Original Manufactured') WHERE SUBSTRING (vin, 5, 1) = (select letter_code from vehicle_model where model_name = 'Responderator') AND vin NOT IN (select vin from vehicle where created >= (select created from vehicle where vin = '7F7ADR311MER00019')) AND vin IN (select vin from vehicle_parts_installed where part_type = 'Comm' and part_number != '004280');
-- discoboard/pre-KERS Sensor switch
UPDATE vehicle SET model_release_id = (select model_release_id from vehicle_model_release where description = 'Responderator: Discoboard') WHERE SUBSTRING (vin, 5, 1) = (select letter_code from vehicle_model where model_name = 'Responderator') AND vin NOT IN (select vin from vehicle where created >= (select created from vehicle where vin = '7F7ADR311MER00019')) AND vin IN (select vin from vehicle_parts_installed where part_type = 'Comm' and part_number = '004280');
-- post KERS Sensor switch
UPDATE vehicle SET model_release_id = (select model_release_id from vehicle_model_release where description = 'Responderator: KERS Sensor') WHERE SUBSTRING (vin, 5, 1) = (select letter_code from vehicle_model where model_name = 'Responderator') AND vin IN (select vin from vehicle where created >= (select created from vehicle where vin = '7F7ADR311MER00019'));

-- Roadster
-- pre discoboard
UPDATE vehicle SET model_release_id = (select model_release_id from vehicle_model_release where description = 'Roadster: Original Manufactured') WHERE SUBSTRING (vin, 5, 1) = (select letter_code from vehicle_model where model_name = 'Roadster') AND vin NOT IN (select vin from vehicle where created >= (select created from vehicle where vin = '7F7ADR311MER00019')) AND vin IN (select vin from vehicle_parts_installed where part_type = 'Comm' and part_number != '004280');
-- discoboard/pre-KERS Sensor switch
UPDATE vehicle SET model_release_id = (select model_release_id from vehicle_model_release where description = 'Roadster: Discoboard') WHERE SUBSTRING (vin, 5, 1) = (select letter_code from vehicle_model where model_name = 'Roadster') AND vin NOT IN (select vin from vehicle where created >= (select created from vehicle where vin = '7F7ADR311MER00019')) AND vin IN (select vin from vehicle_parts_installed where part_type = 'Comm' and part_number = '004280');
-- post KERS Sensor switch
UPDATE vehicle SET model_release_id = (select model_release_id from vehicle_model_release where description = 'Roadster: KERS Sensor') WHERE SUBSTRING (vin, 5, 1) = (select letter_code from vehicle_model where model_name = 'Roadster') AND vin IN (select vin from vehicle where created >= (select created from vehicle where vin = '7F7ADR311MER00019'));

-- remove 004280 part firmware double record bug
DELETE FROM vehicle_firmware_installed WHERE firmware_component = '004280 Comm Bootloader' OR firmware_component = '004280 Comm Firmware';
