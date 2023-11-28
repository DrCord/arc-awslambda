
create table notes (
                note_id serial not null, 
                object_type VARCHAR not null, -- "Vehicle" or "Authority"
                object_id VARCHAR not null,   -- VIN or authority_keys_id (converted to text)
                created timestamp default NOW() not null,
                author text not null,
                content text not null
);

create table notes_tags (
                tag_id serial not null, 
                tag_name text unique not null,
                PRIMARY KEY (tag_id)
);

-- junction table
create table notes_tags_join (
                note_id int not null, 
                tag_id int not null,
                PRIMARY KEY (note_id, tag_id)
);
