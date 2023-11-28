-- create the AuthorityKeys table
create table authority_keys (
                        authority_keys_id serial primary key,
                        parent_authority_id integer not null,
                        cmk_id text not null,
                        public_key bytea not null,
                        encrypted_private_key bytea not null,
                        description text not null
                    );

insert into authority_keys (parent_authority_id, cmk_id, public_key, encrypted_private_key, description) VALUES (0, '0e6e6f67-26ba-48cc-9788-4acab6de74bb', '', '', 'Arcimoto, Inc.');
-- this requires that rekey_authority lambda is run for the Arcimoto authority (authority_id == 1) after initial db bootstrap

-- create the VehicleAuthority mapping table
create table vehicle_authority (
                        authority_id integer,
                        vin text,
                        PRIMARY KEY (authority_id, vin)
                    );

-- create vehicle meta table
create table vehicle_meta (
                    vin text,
                    section text,
                    key text,
                    value text not null,
                    PRIMARY KEY (vin, section, key)
                );