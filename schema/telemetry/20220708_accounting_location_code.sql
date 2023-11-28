CREATE TABLE accounting_location_code (
	id serial PRIMARY KEY,
	code VARCHAR ( 10 ) UNIQUE NOT NULL 
	
);

CREATE TABLE location_join_accounting_location_code (
   location_id int,     				  -- NOT NULL due to PK below
   accounting_location_code_id  int ,     -- NOT NULL due to PK below
   PRIMARY KEY (location_id, accounting_location_code_id)
);

ALTER TABLE location_join_accounting_location_code ADD FOREIGN KEY (location_id)
REFERENCES locations(id) ON DELETE CASCADE;
ALTER TABLE location_join_accounting_location_code ADD FOREIGN KEY (accounting_location_code_id)
REFERENCES accounting_location_code(id) ON DELETE CASCADE;

INSERT INTO accounting_location_code(code)
values	

('OR-EU-HQ'),
('OR-EU-AI'),
('CA-SD-AI'),
('FL-OL-AI'),
('HI-MU-AI'),
('CA-CT-AI'),
('FL-HC-AI'),
('AZ-SC-DC'),
('HI-MU-GC'),
('CA-LA-RF'),
('CA-SM-RF'),
('FL-SP-SS'),
('FL-MI-RF'),
('FL-DV-AC'),
('FL-MI-IB'),
('OR-EU-GT'),
('WA-FH-SM'),
('FL-SS-IH'),
('CA-SD-GC')