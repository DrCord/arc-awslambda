-- create missing foreign keys
ALTER TABLE firmware_release ADD FOREIGN KEY (part_type) REFERENCES vehicle_part_types (part_type) ON UPDATE CASCADE;
ALTER TABLE vehicle_firmware_installed ADD FOREIGN KEY (part_type) REFERENCES vehicle_part_types (part_type) ON UPDATE CASCADE;
ALTER TABLE vehicle_parts_installed ADD FOREIGN KEY (part_type) REFERENCES vehicle_part_types (part_type) ON UPDATE CASCADE;

-- create vehicle_platform
CREATE TABLE vehicle_platform (
  id SERIAL PRIMARY KEY NOT NULL,
  platform_name varchar(20) NOT NULL,
  description text NOT NULL,
  created timestamp NOT NULL DEFAULT NOW()
);

-- vehicle_model table setup
CREATE TABLE vehicle_model (
  id SERIAL PRIMARY KEY NOT NULL,
  model_name varchar(20) NOT NULL,
  letter_code varchar(10) NOT NULL,
  platform_id INT NOT NULL,
  description text NOT NULL,
  created timestamp NOT NULL DEFAULT NOW()
);
ALTER TABLE vehicle_model ADD FOREIGN KEY (platform_id) REFERENCES vehicle_platform (id) ON DELETE CASCADE ON UPDATE CASCADE;

-- vehicle_model_release table
ALTER TABLE vehicle_model_release ADD COLUMN model_id INT DEFAULT NULL;  -- needs to be null due to existing data
ALTER TABLE vehicle_model_release ADD FOREIGN KEY (model_id) REFERENCES vehicle_model (id) ON DELETE CASCADE ON UPDATE CASCADE;

-- remove vehicle_parts_current table (and things that use it) in favor of vehicle_model_parts lookup based on vehicle -> model_release_id
DROP TABLE vehicle_parts_current;
