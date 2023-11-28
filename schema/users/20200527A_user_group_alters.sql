-- fix user_permission_group_join to use proper user_permission compound key
ALTER TABLE user_permission_group_join
    ADD COLUMN resource text not null default '*';

ALTER TABLE user_permission_group_join
    DROP CONSTRAINT user_permission_group_join_pkey;

ALTER TABLE user_permission_group_join
    ADD CONSTRAINT user_permission_group_join_pkey PRIMARY KEY (permission, resource, group_id);

-- enforce foreign key contraints on join table
ALTER TABLE user_permission_group_join 
    ADD CONSTRAINT user_permission_permission_fkey
    FOREIGN KEY (permission, resource) REFERENCES user_permission(permission,resource);

ALTER TABLE user_permission_group_join
    ADD CONSTRAINT user_permission_group_id_fkey
    FOREIGN KEY (group_id) REFERENCES user_group(id);

-- add machine_name column to user_group table
ALTER TABLE user_group
    ADD COLUMN machine_name VARCHAR(200) not null;
