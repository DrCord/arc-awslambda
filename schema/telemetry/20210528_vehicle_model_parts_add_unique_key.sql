ALTER TABLE vehicle_model_parts ADD CONSTRAINT vehicle_model_parts_model_release_id_part_type_ukey UNIQUE(model_release_id, part_type);