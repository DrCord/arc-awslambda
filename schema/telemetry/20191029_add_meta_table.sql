-- create recall meta table
create table meta (
                    section text,
                    key text,
                    value text not null,
                    PRIMARY KEY (section, key)
                  );
