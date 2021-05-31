DROP TABLE IF EXISTS assessor_evaluation;

CREATE TABLE assessor_evaluation(id integer NOT NULL, code varchar(255), description varchar(255), PRIMARY KEY(id));

INSERT INTO assessor_evaluation(id, code, description) VALUES (1, 'LAWB', '8LAW BLDG');
INSERT INTO assessor_evaluation(id, code, description) VALUES (2, 'COMB', 'COMM BLDG');
INSERT INTO assessor_evaluation(id, code, description) VALUES (3, 'COMM', 'COMMERCL');
INSERT INTO assessor_evaluation(id, code, description) VALUES (4, 'EXEM', 'EXEMPT');
INSERT INTO assessor_evaluation(id, code, description) VALUES (5, 'FARM', 'FARM');
INSERT INTO assessor_evaluation(id, code, description) VALUES (6, 'INDU', 'INDUSTRL');
INSERT INTO assessor_evaluation(id, code, description) VALUES (7, 'MXUB', 'MX U BLDG');
INSERT INTO assessor_evaluation(id, code, description) VALUES (8, 'RESB', 'RES BLDG');
INSERT INTO assessor_evaluation(id, code, description) VALUES (9, 'RESI', 'RESIDENTL');
INSERT INTO assessor_evaluation(id, code, description) VALUES (10, 'TSAB', 'TSA BLDG');

ALTER TABLE assessor_evaluation MODIFY COLUMN id integer NOT NULL AUTO_INCREMENT;

DROP TABLE IF EXISTS land_use;

CREATE TABLE land_use(id integer NOT NULL, code varchar(255), description varchar(255), PRIMARY KEY(id));

INSERT INTO land_use(id, code, description) VALUES (1, '100', '');
INSERT INTO land_use(id, code, description) VALUES (2, '200', '');
INSERT INTO land_use(id, code, description) VALUES (3, '202', '');
INSERT INTO land_use(id, code, description) VALUES (4, '203', '');
INSERT INTO land_use(id, code, description) VALUES (5, '204', '');
INSERT INTO land_use(id, code, description) VALUES (6, '205', '');
INSERT INTO land_use(id, code, description) VALUES (7, '300', '');
INSERT INTO land_use(id, code, description) VALUES (8, '400', '');
INSERT INTO land_use(id, code, description) VALUES (9, '600', '');
INSERT INTO land_use(id, code, description) VALUES (10, '1000', '');
INSERT INTO land_use(id, code, description) VALUES (11, '1200', '');
INSERT INTO land_use(id, code, description) VALUES (12, '1300', '');
INSERT INTO land_use(id, code, description) VALUES (13, '1320', '');
INSERT INTO land_use(id, code, description) VALUES (14, '1400', '');
INSERT INTO land_use(id, code, description) VALUES (15, '1410', '');
INSERT INTO land_use(id, code, description) VALUES (16, '2300', '');
INSERT INTO land_use(id, code, description) VALUES (17, '2400', '');
INSERT INTO land_use(id, code, description) VALUES (18, '3300', '');
INSERT INTO land_use(id, code, description) VALUES (19, '7000', '');
INSERT INTO land_use(id, code, description) VALUES (20, '7100', '');
INSERT INTO land_use(id, code, description) VALUES (21, '7200', '');
INSERT INTO land_use(id, code, description) VALUES (22, '7400', '');
INSERT INTO land_use(id, code, description) VALUES (23, '7500', '');
INSERT INTO land_use(id, code, description) VALUES (24, '7600', '');
INSERT INTO land_use(id, code, description) VALUES (25, '7800', '');
INSERT INTO land_use(id, code, description) VALUES (26, '7900', '');
INSERT INTO land_use(id, code, description) VALUES (27, '8000', '');
INSERT INTO land_use(id, code, description) VALUES (28, '8200', '');
INSERT INTO land_use(id, code, description) VALUES (29, '8360', '');
INSERT INTO land_use(id, code, description) VALUES (30, '8400', '');

ALTER TABLE land_use MODIFY COLUMN id integer NOT NULL AUTO_INCREMENT;
