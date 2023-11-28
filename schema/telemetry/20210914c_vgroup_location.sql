CREATE TABLE vehicle_group_join_locations(
  group_id SMALLINT PRIMARY KEY CHECK (group_id > 0),
  location_id SMALLINT NOT NULL CHECK (location_id > 0)
);

ALTER TABLE vehicle_group_join_locations ADD FOREIGN KEY (group_id) REFERENCES vehicle_group (id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE vehicle_group_join_locations ADD FOREIGN KEY (location_id) REFERENCES locations (id) ON DELETE CASCADE ON UPDATE CASCADE;
