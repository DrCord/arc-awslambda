ALTER TABLE vehicle_group_join_accounting_department_code 
    ADD CONSTRAINT vgjadc_vehicle_group_id_unique UNIQUE (vehicle_group_id);
ALTER TABLE location_join_accounting_location_code 
    ADD CONSTRAINT ljalc_location_id_unique UNIQUE (location_id);
