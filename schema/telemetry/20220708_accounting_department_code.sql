
CREATE TABLE accounting_department_code (
	id serial PRIMARY KEY,
	code VARCHAR ( 8 ) UNIQUE NOT NULL ,
	description varchar (64)
	
);

CREATE TABLE vehicle_group_join_accounting_department_code (
   vehicle_group_id int,     				 -- NOT NULL due to PK below
   accounting_department_code_id  int ,     -- NOT NULL due to PK below
   PRIMARY KEY (vehicle_group_id, accounting_department_code_id)
);

ALTER TABLE vehicle_group_join_accounting_department_code ADD FOREIGN KEY (vehicle_group_id)
REFERENCES vehicle_group(id) ON DELETE CASCADE;
ALTER TABLE vehicle_group_join_accounting_department_code ADD FOREIGN KEY (accounting_department_code_id)
REFERENCES accounting_department_code(id) ON DELETE CASCADE;

INSERT INTO accounting_department_code(code, description)
values	

('510', 'Manufacturing'),
('520', 'Fabrication'),
('530', 'Manufacturing Engineering'),
('540', 'Materials'),
('550', 'Quality'),
('560', 'Battery'),
('610', 'Customer Experience'),
('630', 'Creative Marketing'),
('640', 'Sales'),
('650', 'Product Support'),
('660', 'Logistics'),
('670', 'Rental Operations'),
('710', 'Engineering'),
('720', 'Research & Development'),
('730', 'Regulatory Affairs'),
('740', 'CEO'),
('750', 'Tilting Motor Works'),
('810', 'Accounting'),
('820', 'Administration'),
('830', 'Human Resources'),
('840', 'Technology Infrastructure'),
('850', 'Strategic Affairs')
