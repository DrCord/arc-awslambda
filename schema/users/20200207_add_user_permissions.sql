create table user_profile (
    username varchar(200) not null primary key
);

create table user_group (
    id serial primary key,
    name text not null
);

create table user_group_join (
    username varchar(200) not null,
    group_id integer not null,
    PRIMARY KEY (username, group_id)
);

create table user_permission (
    permission varchar(200) not null primary key,
    resource text not null default '*',
    description text not null
);

create table user_permission_group_join (
    permission varchar(200) not null,
    group_id integer not null,
    PRIMARY KEY (permission, group_id)
);