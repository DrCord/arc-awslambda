-- create the vehicle table
create table vehicle (
                    vin text primary key,
                    created timestamp default NOW()
                    );

-- create group table
create table vehicle_group (
                    id serial primary key,
                    name text not null
                );
-- insert Arcimoto into vehicle group table
insert into vehicle_group (name) values ('Arcimoto');

-- create vehicle vehicle group join table
create table vehicle_join_vehicle_group (
                    vin text,
                    group_id integer,
                    PRIMARY KEY (vin, group_id)
                );

-- create vehicle meta table
create table vehicle_meta (
                    vin text,
                    section text,
                    key text,
                    value text not null,
                    PRIMARY KEY (vin, section, key)
                );

-- create telemetry_points table
create table telemetry_points (
                    vin text,
                    prop text,
                    freq text,
                    PRIMARY KEY (vin, prop)
                );
