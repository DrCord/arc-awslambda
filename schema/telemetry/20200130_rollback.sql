-- drop all tsb tables - used to rollback to pre-tsb tables db state
DROP table tsb, tsb_remedies, vehicle_tsb;

-- remove tsb_id_reference column in recalls table
ALTER TABLE recalls DROP COLUMN tsb_id_reference;
