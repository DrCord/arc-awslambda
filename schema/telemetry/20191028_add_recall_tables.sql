-- create the recall table
create table recalls (
                       id serial primary key,
                       mfr_campaign_id text,
                       country text default 'USA', -- uses ISO 3166-1 alpha-3 - https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
                       title text not NULL,
                       description text not NULL,
                       nhtsa_number text not NULL,
                       date timestamp default NOW(),
                       remedy_id integer default NULL, -- link to remedy table -> id column
                       safety_recall boolean default FALSE,
                       safety_description text default NULL,
                       status text default 'active' not NULL
                     );

-- create the remedy table
create table recall_remedies (
                               id serial primary key,
                               date timestamp default NOW(),
                               description text not NULL
                             );

-- create the recall_vins table
create table vehicle_recalls (
                               id serial primary key,
                               recall_id integer not NULL, -- link to recall table -> id column
                               service_date timestamp default NULL,
                               service_reference text not NULL,
                               vin text not NULL -- link to vehicles table -> vin column
                             );
