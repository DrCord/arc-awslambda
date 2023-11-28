insert into authority_keys (parent_authority_id, cmk_id, public_key, encrypted_private_key, description) VALUES (1, '0e6e6f67-26ba-48cc-9788-4acab6de74bb', '', '', 'Q&RA');
insert into authority_keys (parent_authority_id, cmk_id, public_key, encrypted_private_key, description) VALUES (1, '0e6e6f67-26ba-48cc-9788-4acab6de74bb', '', '', 'Engineering');
-- this requires that rekey_authority lambda is run for the each new authority ([2, 3].includes(authority_id)) after initial db bootstrap
