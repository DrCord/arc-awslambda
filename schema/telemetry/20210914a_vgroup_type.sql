CREATE TABLE vehicle_group_type (
  id SERIAL PRIMARY KEY NOT NULL,
  group_type varchar(20) DEFAULT NULL
);

INSERT INTO vehicle_group_type (group_type) VALUES ('internal');
INSERT INTO vehicle_group_type (group_type) VALUES ('pilot');
INSERT INTO vehicle_group_type (group_type) VALUES ('rental');

CREATE TABLE vehicle_group_join_vehicle_group_type(
  group_id SMALLINT PRIMARY KEY CHECK (group_id > 0),
  type_id SMALLINT NOT NULL CHECK (type_id > 0)
);

ALTER TABLE vehicle_group_join_vehicle_group_type ADD FOREIGN KEY (group_id) REFERENCES vehicle_group (id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE vehicle_group_join_vehicle_group_type ADD FOREIGN KEY (type_id) REFERENCES vehicle_group_type (id) ON DELETE CASCADE ON UPDATE CASCADE;
