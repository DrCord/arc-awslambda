-- INSERT INTO recalls (mfr_campaign_id, title, description, nhtsa_number, date, remedy_id, safety_recall, safety_description) VALUES (mfr_campaign_id, title, description, nhtsa_number, '2018-12-31 00:00:00.000000', remedy_id, safety_recall, safety_description);
-- INSERT INTO recall_remedies (date, description) VALUES (date, description);
-- INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (recall_id, service_date, service_reference, vin);
-- updated data
INSERT INTO meta (section, key, value) VALUES ('recall_data_update', '0', '2017-01-01 00:00:00.000000+00');
INSERT INTO meta (section, key, value) VALUES ('recall_data_update', '1', NOW());

-- REMEDIES
INSERT INTO recall_remedies (date, description) VALUES ('2018-12-28 00:00:00.000000', 'Arcimoto has notified all affected owners and the motorcycles are within the manufacturer''s control. Arcimoto will replace the vehicle with a fully compliant one, free of charge. Owners may contact Arcimoto customer service at 1-541-683-6293. Arcimoto''s number for this recall is 7F7-X7F9K-12.'); -- 18V936
INSERT INTO recall_remedies (date, description) VALUES ('2018-12-31 00:00:00.000000', 'Arcimoto has contacted the owners and will replace the existing brake lines with new brake lines that have an updated design, free of charge. Owners may contact Arcimoto customer service at 1-541-683-6293. Arcimoto''s number for this recall is 7F7-P2S8D-12.'); -- 18V937
INSERT INTO recall_remedies (date, description) VALUES ('2018-12-31 00:00:00.000000', 'Arcimoto has notified all affected owners and the motorcycles are within the manufacturer''s control. Arcimoto will update the service brake warning light software, free of charge. Owners may contact Arcimoto customer service at 1-541-683-6293. Arcimoto''s number for this recall is 7F7-H7M4W-12.'); -- 18V938
INSERT INTO recall_remedies (date, description) VALUES ('2018-12-31 00:00:00.000000', 'Arcimoto has notified all affected owners and the motorcycles are within the manufacturer''s control. Arcimoto will replace the vehicles, free of charge. Owners may contact Arcimoto customer service at 541-683-6293. Arcimoto''s number for this recall is 7F7-W3A5M-12.'); -- 18V939
INSERT INTO recall_remedies (date, description) VALUES ('2018-12-31 00:00:00.000000', 'Arcimoto has notified all affected owners and the motorcycles are within the manufacturer''s control. Arcimoto will inspect and replace all the incorrect fittings with the correct ones, as necessary, free of charge. Owners may contact Arcimoto customer service at 1-541-683-6293. Arcimoto''s number for this recall is 7F7-Y8A4X-12.'); -- 18V940
INSERT INTO recall_remedies (date, description) VALUES ('2018-12-31 00:00:00.000000', 'Arcimoto has notified all affected owners and the motorcycles are within the manufacturer''s control. Arcimoto will add identical signal lights to a location in front of the existing ones, free of charge. Owners may contact Arcimoto customer service at 1-541-683-6293. Arcimoto''s number for this recall is 7F7-P5R6U-12.'); -- 18V941
INSERT INTO recall_remedies (date, description) VALUES ('2018-12-31 00:00:00.000000', 'Arcimoto has notified all affected owners and the motorcycles are within the manufacturer''s control. Arcimoto will add a reflex reflector to each side of the vehicle, free of charge. Owners may contact Arcimoto customer service at 1-541-683-6293. Arcimoto''s number for this recall is 7F7-H6Y7W-12.'); -- 18V942
INSERT INTO recall_remedies (date, description) VALUES ('2018-12-31 00:00:00.000000', 'Arcimoto has notified all affected owners and the motorcycles are within the manufacturer''s control. Arcimoto will replace the headlights with supplemental amber marker lights and add fully compliant headlights to the center of the vehicle, mounted to the frame, free of charge. The recall began January 14, 2019. Owners may contact Arcimoto customer service at 1-541-683-6293. Arcimoto''s number for this recall is 7F7-P6J5F-12.'); -- 18V943
INSERT INTO recall_remedies (date, description) VALUES ('2018-12-31 00:00:00.000000', 'Arcimoto has notified all affected owners and the motorcycles are within the manufacturer''s control. Arcimoto will replace the vehicles, free of charge. Owners may contact Arcimoto customer service at 1-541-683-6293. Arcimoto''s number for this recall is 7F7-P4G2A-12.'); -- 18V944
INSERT INTO recall_remedies (date, description) VALUES ('2018-12-31 00:00:00.000000', 'Arcimoto has notified all affected owners and the motorcycles are within the manufacturer''s control. Arcimoto will replace the tie-rods, free of charge. Owners may contact Arcimoto customer service at 1-541-683-6293. Arcimoto''s number for this recall is 7F7-A3N5H-12.'); -- 18V945
INSERT INTO recall_remedies (date, description) VALUES ('2018-12-31 00:00:00.000000', 'Arcimoto has notified all affected owners and the motorcycles are within the manufacturer''s control. Arcimoto will replace the vehicles, free of charge. Owners may contact Arcimoto customer service at 1-541-683-6293. Arcimoto''s number for this recall is 7F7-A3Z5C-12.'); -- 18V946

-- RECALLS
INSERT INTO recalls (mfr_campaign_id, title, description, nhtsa_number, date, remedy_id, safety_recall, safety_description) VALUES ('7F7-X7F9K-12', 'Certification Label Not Applied/Part 567', 'Arcimoto Inc (Arcimoto) is recalling certain 2017-2018 FUV motorcycles. These vehicles were built without a certification label applied and, as such, they fail to comply with the requirements of 49 CFR Part 567, "Certification."', '18V936', '2018-12-28 00:00:00.000000', 1, TRUE, 'The missing label can affect the owner''s ability to determine if a safety recall includes their vehicle. If the owner is not able to verify if their motorcycle is involved in a safety recall, it can increase the risk of injury or crash.');
INSERT INTO recalls (mfr_campaign_id, title, description, nhtsa_number, date, remedy_id, safety_recall, safety_description) VALUES ('7F7-P2S8D-12', 'Excessive Stopping Distance/FMVSS 122', 'Arcimoto Inc (Arcimoto) is recalling certain 2017 FUV motorcycles. The affected motorcycles were built with a front/rear split brake system instead of a left/right split brake system. In the event of a front brake system failure, the rear brake system may not allow the vehicle to meet the minimum stopping distance requirements. As such, these vehicles fail to comply with Federal Motor Safety Standard (FMVSS) number 122, "Motorcycle brake systems."', '18V937', '2018-12-31 00:00:00.000000', 2, TRUE, 'If the brakes cannot stop a the motorcycle within the distance required, there is an increased risk of a crash.');
INSERT INTO recalls (mfr_campaign_id, title, description, nhtsa_number, date, remedy_id, safety_recall, safety_description) VALUES ('7F7-H7M4W-12', 'Brake Warning Light Missing/FMVSS 122', 'Arcimoto Inc (Arcimoto) is recalling certain 2017-2018 FUV motorcycles. The affected motorcycles do not have a service brake warning light to warn the operator if there is a brake system malfunction. As such, these vehicles fail to comply with Federal Motor Safety Standard (FMVSS) number 122, "Motorcycle brake systems."', '18V938', '2018-12-31 00:00:00.000000', 3, TRUE, 'If the operator unknowingly operates the motorcycle with a problem in the brake system, there would be an increased risk of a crash.');
INSERT INTO recalls (mfr_campaign_id, title, description, nhtsa_number, date, remedy_id, safety_recall, safety_description) VALUES ('7F7-W3A5M-12', 'Seat May Collapse In The Event of A Crash', 'Arcimoto Inc (Arcimoto) is recalling certain 2017-2018 FUV motorcycles. In the event of a crash, the seat may not support the driver as intended, preventing the seatbelts from holding the driver in place.', '18V939', '2018-12-31 00:00:00.000000', 4, TRUE, 'If the driver is not properly secured, it can increase the risk of injury in a crash.');
INSERT INTO recalls (mfr_campaign_id, title, description, nhtsa_number, date, remedy_id, safety_recall, safety_description) VALUES ('7F7-Y8A4X-12', 'Brake Fluid Leak Due to Incorrect Brake Fittings', 'Arcimoto Inc (Arcimoto) is recalling certain 2017 FUV motorcycles. Incorrect fittings were installed in the braking system, potentially resulting in a brake fluid leak.', '18V940', '2018-12-31 00:00:00.000000', 5, TRUE, 'A brake fluid leak can reduce brake effectiveness, increasing the risk of a crash.');
INSERT INTO recalls (mfr_campaign_id, title, description, nhtsa_number, date, remedy_id, safety_recall, safety_description) VALUES ('7F7-P5R6U-12', 'Turn Signals Incorrectly Positioned/FMVSS 108', 'Arcimoto Inc (Arcimoto) is recalling certain 2017-2018 FUV motorcycles. The front turn signal lights are not positioned at, or near, the front of the motorcycle as required. As such, these vehicles fail to comply to Federal Motor Vehicle Safety Standard (FMVSS) number 108, "Lamps, Reflective devices, and Associated Equipment."', '18V941', '2018-12-31 00:00:00.000000', 6, TRUE, 'The incorrectly positioned front turn signals can reduce their visibility, increasing the risk of a crash.');
INSERT INTO recalls (mfr_campaign_id, title, description, nhtsa_number, date, remedy_id, safety_recall, safety_description) VALUES ('7F7-H6Y7W-12', 'Reflex Reflector Not In Compliance/FMVSS 108', 'Arcimoto, Inc (Arcimoto) is recalling certain 2017-2018 FUV motorcycles. The combination brake light, tail light, and turn signal assembly does not have a reflex reflector in the side-facing surfaces. As such these vehicles fail to comply with the requirements of Federal Motor Vehicle Safety Standard (FMVSS) number 108, "Lamps, reflective devices, and Associated Equipment."', '18V942', '2018-12-31 00:00:00.000000', 7, TRUE, 'Without rear side reflex reflectors, the vehicle may have less visibility from the side, increasing the risk of a crash.');
INSERT INTO recalls (mfr_campaign_id, title, description, nhtsa_number, date, remedy_id, safety_recall, safety_description) VALUES ('7F7-P6J5F-12', 'Headlamps Positioned too far Apart/FMVSS 108', 'Arcimoto Inc. (Arcimoto) is recalling certain 2017-2018 FUV motorcycles. The headlights on the motorcycles may be spaced too far apart to appear as a motorcycle to oncoming traffic. As a result, the motorcycles fail to comply with Federal Motor Vehicle Safety Standard (FMVSS) number 101, "Lamps, reflective devices, and associated Equipment."', '18V943', '2018-12-31 00:00:00.000000', 8, TRUE, 'Due to the improperly positioned headlamps, the vehicle may not be recognizable as a motorcycle in the dark, increasing the risk of a crash.');
INSERT INTO recalls (mfr_campaign_id, title, description, nhtsa_number, date, remedy_id, safety_recall, safety_description) VALUES ('7F7-P4G2A-12', 'Gearbox May Prematurely Fail', 'Arcimoto, Inc (Arcimoto) is recalling certain 2018 FUV motorcycles. Incorrect machining of the transmission case may result in premature failure of the gearbox.', '18V944', '2018-12-31 00:00:00.000000', 9, TRUE, 'Transmission failure may immobilize the motorcycle, increasing the risk of a crash.');
INSERT INTO recalls (mfr_campaign_id, title, description, nhtsa_number, date, remedy_id, safety_recall, safety_description) VALUES ('7F7-A3N5H-12', 'Possible Loss of Steering Control', 'Arcimoto Inc (Arcimoto) is recalling certain 2017-2018 FUV motorcycles. In the affected vehicles, the front suspension and steering system may loosen or wear, possibly resulting in a loss of steering control.', '18V945', '2018-12-31 00:00:00.000000', 10, TRUE, 'A sudden loss of steering control may increase the risk of a crash.');
INSERT INTO recalls (mfr_campaign_id, title, description, nhtsa_number, date, remedy_id, safety_recall, safety_description) VALUES ('7F7-A3Z5C-12', 'Battery Shutdown May Occur Unexpectedly', 'Arcimoto, Inc (Arcimoto) is recalling certain 2017-2018 FUV motorcycles. Over time, increased resistance at the battery connection may result in the Battery Management System unexpectedly shutting down propulsion power.', '18V946', '2018-12-31 00:00:00.000000', 11, TRUE, 'A sudden loss of propulsion power may increase the risk of a crash.');
INSERT INTO recalls (mfr_campaign_id, title, description, nhtsa_number, date, remedy_id, safety_recall, safety_description) VALUES ('', 'Tie Rods May Separate', 'Arcimoto, Inc. (Arcimoto) is recalling certain Arcimoto FUV motorcycles. There may be insufficient thread engagement between the inner and outer tie rods, possibly resulting in the separation of the tie rod assembly.', '19V728', '2019-10-11 00:00:00.000000', NULL, TRUE, 'A tie rod separation can cause a loss of steering and increase the risk of a crash.');

-- VEHICLE RECALLS
-- 18V936 - recall_id 1
-- INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', 'vin');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, '2019-09-24 00:00:00.000000', '', '7F7ATR317HEB00000');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, '2019-10-01 00:00:00.000000', '', '7F7ATR319HEB00001');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR311JEB00001');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR313JEB00002');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR315JEB00003');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR317JEB00004');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR319JEB00005');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR312JEB00007');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR314JEB00008');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR316JEB00009');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR312JEB00010');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR314JEB00011');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR316JEB00012');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR318JEB00013');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR31XJEB00014');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR311JEB00015');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR313JEB00016');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR315JEB00017');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR317JEB00018');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, '2019-09-24 00:00:00.000000', '', '7F7ATR315JEB00020');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR317JEB00021');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, NULL, '', '7F7ATR319JEB00022');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (1, '2019-10-01 00:00:00.000000', '', '7F7ATR310JEB00023');
-- 18V937 - recall_id 2
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (2, '2019-09-24 00:00:00.000000', '', '7F7ATR317HEB00000');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (2, '2019-10-01 00:00:00.000000', '', '7F7ATR319HEB00001');
-- 18V938 - recall_id 3
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, '2019-09-24 00:00:00.000000', '', '7F7ATR317HEB00000');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, '2019-10-01 00:00:00.000000', '', '7F7ATR319HEB00001');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, NULL, '', '7F7ATR311JEB00001');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, NULL, '', '7F7ATR313JEB00002');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, NULL, '', '7F7ATR315JEB00003');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, NULL, '', '7F7ATR319JEB00005');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, NULL, '', '7F7ATR312JEB00007');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, NULL, '', '7F7ATR314JEB00008');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, NULL, '', '7F7ATR316JEB00009');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, NULL, '', '7F7ATR312JEB00010');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, NULL, '', '7F7ATR314JEB00011');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, NULL, '', '7F7ATR316JEB00012');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, NULL, '', '7F7ATR318JEB00013');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, NULL, '', '7F7ATR31XJEB00014');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, NULL, '', '7F7ATR311JEB00015');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, NULL, '', '7F7ATR313JEB00016');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, NULL, '', '7F7ATR315JEB00017');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, NULL, '', '7F7ATR317JEB00018');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, '2019-09-24 00:00:00.000000', '', '7F7ATR315JEB00020');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, NULL, '', '7F7ATR317JEB00021');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, NULL, '', '7F7ATR319JEB00022');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (3, '2019-10-01 00:00:00.000000', '', '7F7ATR310JEB00023');
-- 18V939 - recall_id 4
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, '2019-09-24 00:00:00.000000', '', '7F7ATR317HEB00000');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, '2019-10-01 00:00:00.000000', '', '7F7ATR319HEB00001');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR311JEB00001');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR313JEB00002');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR315JEB00003');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR317JEB00004');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR319JEB00005');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR312JEB00007');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR314JEB00008');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR316JEB00009');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR312JEB00010');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR314JEB00011');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR316JEB00012');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR318JEB00013');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR31XJEB00014');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR311JEB00015');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR313JEB00016');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR315JEB00017');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR317JEB00018');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, '2019-09-24 00:00:00.000000', '', '7F7ATR315JEB00020');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR317JEB00021');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, NULL, '', '7F7ATR319JEB00022');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (4, '2019-10-01 00:00:00.000000', '', '7F7ATR310JEB00023');
-- 18V940 - recall_id 5
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (5, '2019-09-24 00:00:00.000000', '', '7F7ATR317HEB00000');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (5, '2019-10-01 00:00:00.000000', '', '7F7ATR319HEB00001');
-- 18V941 - recall_id 6
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, '2019-09-24 00:00:00.000000', '', '7F7ATR317HEB00000');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, '2019-10-01 00:00:00.000000', '', '7F7ATR319HEB00001');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, NULL, '', '7F7ATR311JEB00001');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, NULL, '', '7F7ATR313JEB00002');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, NULL, '', '7F7ATR315JEB00003');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, NULL, '', '7F7ATR319JEB00005');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, NULL, '', '7F7ATR312JEB00007');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, NULL, '', '7F7ATR314JEB00008');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, NULL, '', '7F7ATR316JEB00009');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, NULL, '', '7F7ATR312JEB00010');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, NULL, '', '7F7ATR314JEB00011');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, NULL, '', '7F7ATR316JEB00012');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, NULL, '', '7F7ATR318JEB00013');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, NULL, '', '7F7ATR31XJEB00014');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, NULL, '', '7F7ATR311JEB00015');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, NULL, '', '7F7ATR313JEB00016');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, NULL, '', '7F7ATR315JEB00017');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, NULL, '', '7F7ATR317JEB00018');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, '2019-09-24 00:00:00.000000', '', '7F7ATR315JEB00020');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, NULL, '', '7F7ATR317JEB00021');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, NULL, '', '7F7ATR319JEB00022');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (6, '2019-10-01 00:00:00.000000', '', '7F7ATR310JEB00023');
-- 18V942 - recall_id 7
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, '2019-09-24 00:00:00.000000', '', '7F7ATR317HEB00000');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, '2019-10-01 00:00:00.000000', '', '7F7ATR319HEB00001');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, NULL, '', '7F7ATR311JEB00001');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, NULL, '', '7F7ATR313JEB00002');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, NULL, '', '7F7ATR315JEB00003');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, NULL, '', '7F7ATR319JEB00005');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, NULL, '', '7F7ATR312JEB00007');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, NULL, '', '7F7ATR314JEB00008');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, NULL, '', '7F7ATR316JEB00009');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, NULL, '', '7F7ATR312JEB00010');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, NULL, '', '7F7ATR314JEB00011');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, NULL, '', '7F7ATR316JEB00012');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, NULL, '', '7F7ATR318JEB00013');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, NULL, '', '7F7ATR31XJEB00014');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, NULL, '', '7F7ATR311JEB00015');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, NULL, '', '7F7ATR313JEB00016');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, NULL, '', '7F7ATR315JEB00017');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, NULL, '', '7F7ATR317JEB00018');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, '2019-09-24 00:00:00.000000', '', '7F7ATR315JEB00020');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, NULL, '', '7F7ATR317JEB00021');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, NULL, '', '7F7ATR319JEB00022');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (7, '2019-10-01 00:00:00.000000', '', '7F7ATR310JEB00023');
-- 18V943 - recall_id 8
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, '2019-09-24 00:00:00.000000', '', '7F7ATR317HEB00000');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, '2019-10-01 00:00:00.000000', '', '7F7ATR319HEB00001');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, NULL, '', '7F7ATR311JEB00001');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, NULL, '', '7F7ATR313JEB00002');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, NULL, '', '7F7ATR315JEB00003');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, NULL, '', '7F7ATR319JEB00005');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, NULL, '', '7F7ATR312JEB00007');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, NULL, '', '7F7ATR314JEB00008');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, NULL, '', '7F7ATR316JEB00009');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, NULL, '', '7F7ATR312JEB00010');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, NULL, '', '7F7ATR314JEB00011');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, NULL, '', '7F7ATR316JEB00012');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, NULL, '', '7F7ATR318JEB00013');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, NULL, '', '7F7ATR31XJEB00014');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, NULL, '', '7F7ATR311JEB00015');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, NULL, '', '7F7ATR313JEB00016');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, NULL, '', '7F7ATR315JEB00017');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, NULL, '', '7F7ATR317JEB00018');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, '2019-09-24 00:00:00.000000', '', '7F7ATR315JEB00020');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, NULL, '', '7F7ATR317JEB00021');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, NULL, '', '7F7ATR319JEB00022');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (8, '2019-10-01 00:00:00.000000', '', '7F7ATR310JEB00023');
-- 18V944 - recall_id 9
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (9, NULL, '', '7F7ATR316JEB00009');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (9, NULL, '', '7F7ATR312JEB00010');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (9, NULL, '', '7F7ATR314JEB00011');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (9, NULL, '', '7F7ATR316JEB00012');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (9, NULL, '', '7F7ATR318JEB00013');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (9, NULL, '', '7F7ATR31XJEB00014');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (9, NULL, '', '7F7ATR311JEB00015');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (9, NULL, '', '7F7ATR313JEB00016');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (9, NULL, '', '7F7ATR315JEB00017');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (9, NULL, '', '7F7ATR317JEB00018');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (9, '2019-09-24 00:00:00.000000', '', '7F7ATR315JEB00020');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (9, NULL, '', '7F7ATR317JEB00021');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (9, NULL, '', '7F7ATR319JEB00022');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (9, '2019-10-01 00:00:00.000000', '', '7F7ATR310JEB00023');
-- 18V945 - recall_id 10
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, '2019-09-24 00:00:00.000000', '', '7F7ATR317HEB00000');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, '2019-10-01 00:00:00.000000', '', '7F7ATR319HEB00001');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, NULL, '', '7F7ATR311JEB00001');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, NULL, '', '7F7ATR313JEB00002');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, NULL, '', '7F7ATR315JEB00003');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, NULL, '', '7F7ATR319JEB00005');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, NULL, '', '7F7ATR312JEB00007');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, NULL, '', '7F7ATR314JEB00008');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, NULL, '', '7F7ATR316JEB00009');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, NULL, '', '7F7ATR312JEB00010');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, NULL, '', '7F7ATR314JEB00011');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, NULL, '', '7F7ATR316JEB00012');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, NULL, '', '7F7ATR318JEB00013');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, NULL, '', '7F7ATR31XJEB00014');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, NULL, '', '7F7ATR311JEB00015');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, NULL, '', '7F7ATR313JEB00016');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, NULL, '', '7F7ATR315JEB00017');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, NULL, '', '7F7ATR317JEB00018');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, '2019-09-24 00:00:00.000000', '', '7F7ATR315JEB00020');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, NULL, '', '7F7ATR317JEB00021');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, NULL, '', '7F7ATR319JEB00022');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (10, '2019-10-01 00:00:00.000000', '', '7F7ATR310JEB00023');
-- 18V946 - recall_id 11
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, '2019-09-24 00:00:00.000000', '', '7F7ATR317HEB00000');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, '2019-10-01 00:00:00.000000', '', '7F7ATR319HEB00001');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR311JEB00001');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR313JEB00002');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR315JEB00003');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR317JEB00004');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR319JEB00005');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR312JEB00007');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR314JEB00008');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR316JEB00009');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR312JEB00010');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR314JEB00011');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR316JEB00012');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR318JEB00013');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR31XJEB00014');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR311JEB00015');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR313JEB00016');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR315JEB00017');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR317JEB00018');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, '2019-09-24 00:00:00.000000', '', '7F7ATR315JEB00020');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR317JEB00021');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, NULL, '', '7F7ATR319JEB00022');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (11, '2019-10-01 00:00:00.000000', '', '7F7ATR310JEB00023');
-- 19V728 - recall_id 12
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (12, '2019-10-17 00:00:00.000000', '', '7F7ATR312KER00000');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (12, NULL, '', '7F7ATR314KER00001');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (12, '2019-10-14 00:00:00.000000', '', '7F7ATR316KER00002');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (12, NULL, '', '7F7ATR318KER00003');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (12, NULL, '', '7F7ATR31XKER00004');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (12, '2019-10-15 00:00:00.000000', '', '7F7ATR311KER00005');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (12, NULL, '', '7F7ATR313KER00006');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (12, NULL, '', '7F7ATR315KER00007');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (12, '2019-10-16 00:00:00.000000', '', '7F7ATR317KER00008');
INSERT INTO vehicle_recalls (recall_id, service_date, service_reference, vin) VALUES (12, NULL, '', '7F7ATR319KER00009');