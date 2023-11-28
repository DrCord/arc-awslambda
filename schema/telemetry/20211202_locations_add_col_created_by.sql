-- add created_by column to locations table
ALTER TABLE locations ADD COLUMN created_by varchar(200) default NULL;