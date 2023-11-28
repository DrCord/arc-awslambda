-- create the tsb (technical service bulletins) table
create table tsb (
                       id serial primary key,
                       country text default 'USA', -- uses ISO 3166-1 alpha-3 - https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
                       title text not NULL,
                       description text not NULL,
                       date timestamp default NOW(),
                       remedy_id integer default NULL, -- link to tsb_remedies table -> id column
                       status text default 'active' not NULL,
                       recall_id_reference integer default NULL
                     );

-- create the tsb_remedies table
create table tsb_remedies (
                               id serial primary key,
                               date timestamp default NOW(),
                               description text not NULL
                             );

-- create the vehicle_tsb table
create table vehicle_tsb (
                               id serial primary key,
                               tsb_id integer not NULL, -- link to tsb table -> id column
                               service_date timestamp default NULL,
                               service_reference text not NULL,
                               vin text not NULL -- link to vehicles table -> vin column
                             );

-- add tsb_id_reference column to recalls table
ALTER TABLE recalls ADD COLUMN tsb_id_reference integer default NULL;