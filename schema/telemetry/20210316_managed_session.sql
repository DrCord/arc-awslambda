CREATE TABLE managed_sessions_vehicles (
  vin varchar(50) PRIMARY KEY NOT NULL
);

CREATE TABLE managed_sessions (
  id SERIAL PRIMARY KEY NOT NULL,
  vin varchar(50) NOT NULL,
  pin char(6) NOT NULL,
  initialization timestamp NOT NULL DEFAULT NOW(),
  completion timestamp DEFAULT NULL,
  creator varchar(200) NOT NULL
);
