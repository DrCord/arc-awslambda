-- existing vehicle data forces us to allow NULL to start, we might alter this to not null after data is in place
ALTER TABLE vehicle ADD COLUMN model_release_id integer default NULL;

CREATE TABLE vehicle_parts_installed (
  vin varchar(50),
  part_type varchar(50),
  part_number varchar(50),
  installed timestamp NOT NULL DEFAULT NOW(),
  PRIMARY KEY (vin, part_type)
);

CREATE TABLE vehicle_firmware_installed (
  vin varchar(50),
  part_type varchar(50),
  firmware_component varchar(50),
  firmware_release_id int,
  installed timestamp NOT NULL DEFAULT NOW(),
  PRIMARY KEY (vin, part_type, firmware_component)
);

CREATE TABLE vehicle_parts_current (
  model_release_id int NOT NULL,
  part_type varchar(50),
  part_number varchar(50),
  created timestamp NOT NULL DEFAULT NOW(),
  PRIMARY KEY (model_release_id, part_type)
);

CREATE TABLE vehicle_model_release (
  model_release_id SERIAL PRIMARY KEY NOT NULL,
  description text NOT NULL,
  created timestamp NOT NULL DEFAULT NOW()
);

CREATE TABLE vehicle_model_parts (
  model_release_id int NOT NULL,
  part_type varchar(50),
  part_number varchar(50),
  firmware_release_id int DEFAULT null,
  created timestamp NOT NULL DEFAULT NOW(),
  PRIMARY KEY (model_release_id, part_type, part_number)
);

CREATE TABLE firmware_release (
  firmware_release_id SERIAL PRIMARY KEY NOT NULL,
  part_type varchar(50),
  firmware_component varchar(50),
  description text,
  version text,
  hash varchar(64),
  created timestamp NOT NULL DEFAULT NOW(),
  UNIQUE (firmware_component, hash)
);

CREATE TABLE vehicle_part_types (
  part_type varchar(50) PRIMARY KEY NOT NULL
);

CREATE TABLE firmware_components (
  part_type varchar(50),
  firmware_component varchar(50),
  created timestamp NOT NULL DEFAULT NOW(),
  PRIMARY KEY (part_type, firmware_component)
);

ALTER TABLE vehicle ADD FOREIGN KEY (model_release_id) REFERENCES vehicle_model_release (model_release_id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE vehicle_parts_installed ADD FOREIGN KEY (vin) REFERENCES vehicle (vin) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE vehicle_firmware_installed ADD FOREIGN KEY (vin) REFERENCES vehicle (vin) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE vehicle_firmware_installed ADD FOREIGN KEY (firmware_release_id) REFERENCES firmware_release (firmware_release_id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE vehicle_parts_current ADD FOREIGN KEY (model_release_id) REFERENCES vehicle_model_release (model_release_id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE vehicle_model_parts ADD FOREIGN KEY (model_release_id) REFERENCES vehicle_model_release (model_release_id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE vehicle_model_parts ADD FOREIGN KEY (firmware_release_id) REFERENCES firmware_release (firmware_release_id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE vehicle_model_parts ADD FOREIGN KEY (part_type) REFERENCES vehicle_part_types (part_type) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE firmware_components ADD FOREIGN KEY (part_type) REFERENCES vehicle_part_types (part_type) ON DELETE CASCADE ON UPDATE CASCADE;
