DROP table recalls;
DROP table recall_remedies;
DROP table vehicle_recalls;

DELETE FROM meta where section = 'recall_data_update';
-- You must run the 20191028_add_recall_tables.sql file to recreate the recalls table after after running this file.
-- Dropping and recreating the tables gets around having to reset the sequence for each table.