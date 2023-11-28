CREATE TABLE managed_sessions_reef (
  id SERIAL PRIMARY KEY NOT NULL,
  vin varchar(50) NOT NULL,
  pin char(6) NOT NULL,
  initialization timestamp NOT NULL DEFAULT NOW(),
  completion timestamp DEFAULT NULL,
  verification_id varchar(50)
);
