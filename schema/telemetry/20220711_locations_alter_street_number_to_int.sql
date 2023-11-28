-- alter street_number column from locations table to int
-- create new column and migrate data to minimize downtime
ALTER TABLE locations ADD COLUMN street_number_int integer;
UPDATE locations SET street_number_int = street_number;
-- transaction to drop old column and rename new
BEGIN TRANSACTION;
-- explicitly lock the table against other changes (safety)
LOCK TABLE locations IN EXCLUSIVE MODE;
-- drop and rename the columns
ALTER TABLE locations DROP COLUMN street_number;
ALTER TABLE locations RENAME COLUMN street_number_int TO street_number;
-- commit to end lock and transaction
COMMIT;