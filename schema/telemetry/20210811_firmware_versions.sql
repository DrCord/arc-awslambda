CREATE TABLE firmware_versions (
  hash varchar(64) PRIMARY KEY NOT NULL,
  firmware_component varchar(50),
  created timestamp NOT NULL DEFAULT NOW()
);

INSERT INTO firmware_versions VALUES ('436d2c6ea5d38c70db06ecf4fc56ba9d4521eaf9', 'Comm Firmware', '2021-05-03T19:39:06+00:00');
INSERT INTO firmware_versions VALUES ('83e5ee96bec12e97d6650cd66e642bdb0e26165d', 'Comm Firmware', '2020-11-09T23:48:41+00:00');
INSERT INTO firmware_versions VALUES ('0a61a952c0b5b512bb6fa74250dedab09fcae7bc', 'Comm Firmware', '2020-10-07T22:03:14+00:00');
INSERT INTO firmware_versions VALUES ('e736bac9216d010621a38436a65582cc00a3231a', 'Comm Firmware', '2020-10-01T22:36:04+00:00');
INSERT INTO firmware_versions VALUES ('47683a421da937ade566c7db958a22992c3a9491', 'Comm Firmware', '2020-01-28T18:20:08+00:00');
INSERT INTO firmware_versions VALUES ('f055745a753d4123b2b704cfade9b0983223c89c', 'Comm Firmware', '2019-12-06T00:28:38+00:00');
INSERT INTO firmware_versions VALUES ('9aab9ef8e31b794d6c56e34cde139899781eb015', 'Comm Firmware', '2019-11-19T23:30:36+00:00');
INSERT INTO firmware_versions VALUES ('c5f331524004f77be37f1da5a332044035e17a3e', 'Comm Firmware', '2019-10-04T17:48:43+00:00');
INSERT INTO firmware_versions VALUES ('33d921203a6346bccb958f1774b0913bc190ad48', 'Comm Firmware', '2019-10-02T22:33:29+00:00');
INSERT INTO firmware_versions VALUES ('c12c0cdd0be3146cc597e199a6adb566495318d0', 'Comm Firmware', '2019-09-26T19:16:22+00:00');
INSERT INTO firmware_versions VALUES ('afb59ff1c589c4851db881ce170d36665e17f9d8', 'Comm Firmware', '2019-09-23T22:03:57+00:00');
INSERT INTO firmware_versions VALUES ('29c103210727d6b05e25e84a956448bab17fa0ee', 'Comm Firmware', '2019-09-19T19:00:16+00:00');
INSERT INTO firmware_versions VALUES ('e544d8b907f86a3dfe97cc4cdf6bc7755578039f', 'Comm Firmware', '2019-09-09T23:06:27+00:00');
INSERT INTO firmware_versions VALUES ('d48e72488e185974134bc67e503545111ce6291d', 'Comm Firmware', '2019-09-06T23:48:03+00:00');
INSERT INTO firmware_versions VALUES ('bd146734570839c86575da233bca852191d50985', 'Comm Firmware', '2019-08-30T16:31:18+00:00');
INSERT INTO firmware_versions VALUES ('a2e7cebf46955e19e02c9ca6895a9e06db564377', 'Comm Firmware', '2019-08-16T00:14:06+00:00');
INSERT INTO firmware_versions VALUES ('7704770bdb09fb1fff4431da4875c88b8a3795b7', 'Comm Firmware', '2019-08-15T22:48:41+00:00');
INSERT INTO firmware_versions VALUES ('56e66534298472203087f8b3fc7110b1cbb78f5b', 'Comm Firmware', '2019-08-15T21:25:57+00:00');
INSERT INTO firmware_versions VALUES ('e0e513071f0be21c6cd18b201093079bc3beaaa0', 'Comm Firmware', '2019-06-11T20:25:49+00:00');
INSERT INTO firmware_versions VALUES ('421880755e12e6eee4e79bea3450d4bbe51dde4c', 'Comm Firmware', '2019-06-07T17:21:32+00:00');
