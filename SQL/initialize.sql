

-- create the schemas to use
CREATE SCHEMA admin;
CREATE SCHEMA laboratory;
CREATE SCHEMA userInfo;

DROP TABLE IF EXISTS admin.Numb3rL0ck3r_institution;
CREATE SEQUENCE institutionid_seq;
CREATE TABLE admin.Numb3rL0ck3r_institution (
       institutionid bigint DEFAULT nextval('institutionid_seq'),
       institutionName text,
       institutionDescription text,
       PRIMARY KEY(institutionid)
);

DROP TABLE IF EXISTS admin.Numb3rL0ck3r_department;
CREATE SEQUENCE departmentid_seq;
CREATE TABLE admin.Numb3rL0ck3r_department (
       departmentid bigint DEFAULT nextval('departmentid_seq'),
       departmentName text,
       departmentDescription text,
       PRIMARY KEY(departmentid)
);

DROP TABLE IF EXISTS admin.Numb3rL0ck3r_laboratory;
CREATE SEQUENCE laboratoryid_seq;
CREATE TABLE admin.Numb3rL0ck3r_laboratory (
       laboratoryid bigint DEFAULT nextval('laboratoryid_seq'),
       laboratoryName text,
       laboratoryDescription text,
       laboratoryDate timestamp DEFAULT CURRENT_TIMESTAMP,
       PRIMARY KEY(laboratoryid)
);

DROP TABLE IF EXISTS admin.Numb3rL0ck3r_laboratoryInstance;
CREATE SEQUENCE laboratoryInstanceid_seq;
CREATE TABLE admin.Numb3rL0ck3r_laboratoryInstance (
       laboratoryInstanceid bigint DEFAULT nextval('laboratoryInstanceid_seq'),
       laboratoryid bigint REFERENCES admin.Numb3rL0ck3r_laboratory(laboratoryid) ON DELETE CASCADE,
       laboratoryInstanceName text,
       laboratoryInstanceDescription text,
       laboratoryInstanceDate timestamp DEFAULT CURRENT_TIMESTAMP,
       PRIMARY KEY(laboratoryInstanceid)
);


DROP TABLE IF EXISTS userInfo.Numb3rL0ck3r_user;
CREATE SEQUENCE userid_seq;
CREATE TABLE userInfo.Numb3rL0ck3r_user (
       userid bigint DEFAULT nextval('userid_seq'),
       username text NOT NULL,
       password text,
       email text NOT NULL,
       originalIPAddress text DEFAULT NULL,
       lastIPAddress text DEFAULT NULL,
       creationDate timestamp DEFAULT CURRENT_TIMESTAMP,
       lastPWChange timestamp DEFAULT CURRENT_TIMESTAMP,
       institutionid bigint REFERENCES admin.Numb3rL0ck3r_institution(institutionid) NOT NULL,
       PRIMARY KEY(userid)
);

DROP TABLE IF EXISTS admin.Numb3rL0ck3r_administrativeRoles;
CREATE SEQUENCE administrativeRolesid_seq;
CREATE TABLE admin.Numb3rL0ck3r_administrativeRoles (
       administrativeRolesid bigint DEFAULT nextval('administrativeRolesid_seq'),
       administrativeRoleTitle text,
       administrativeRolesDescription text,
       PRIMARY KEY(administrativeRolesid)
);

DROP TABLE IF EXISTS admin.Numb3rL0ck3r_priviliges;
CREATE SEQUENCE priviligesid_seq;
CREATE TABLE admin.Numb3rL0ck3r_priviliges (
       priviligesid bigint DEFAULT nextval('priviligesid_seq'),
       userid bigint REFERENCES userInfo.Numb3rL0ck3r_user(userid),
       administrativeRolesid bigint REFERENCES admin.Numb3rL0ck3r_administrativeRoles(administrativeRolesid) ON DELETE CASCADE,
       institutionid bigint REFERENCES admin.Numb3rL0ck3r_institution(institutionid) ON DELETE CASCADE,
       departmentid bigint REFERENCES admin.Numb3rL0ck3r_department(departmentid) ON DELETE CASCADE,
       laboratoryid bigint REFERENCES admin.Numb3rL0ck3r_laboratory(laboratoryid) ON DELETE CASCADE,
       laboratoryInstanceid bigint REFERENCES admin.Numb3rL0ck3r_laboratoryInstance(laboratoryInstanceid) ON DELETE CASCADE,
       PRIMARY KEY(priviligesid)
);

-- select tablename from pg_tables where tablename  ~ '^numb+';



