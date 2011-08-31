

DROP TABLE IF EXISTS Numb3rL0ck3r_user;
CREATE TABLE Numb3rL0ck3r_user (
       userid bigint PRIMARY KEY DEFAULT nextval('user_userid_no_seq'),
       username text NOT NULL,
       password text,
       email text NOT NULL,
       originalIPAddress text DEFAULT NULL,
       lastIPAddress text DEFAULT NULL,
       creationDate timestamp DEFAULT CURRENT_TIMESTAMP,
       lastPWChange timestamp DEFAULT CURRENT_TIMESTAMP,
       institutionid REFERENCES institution(institutionid) NOT NULL
);

DROP TABLE IF EXISTS Numb3rL0ck3r_administrativeRoles;
CREATE TABLE Numb3rL0ck3r_administrativeRoles (
       administrativeRolesid bigint PRIMARY KEY DEFAULT nextval('administrativeRoles_administrativeRolesid_no_seq'),
       administrativeRoleTitle text,
       administrativeRolesDescription text
);

DROP TABLE IF EXISTS Numb3rL0ck3r_priviliges;
CREATE TABLE Numb3rL0ck3r_priviliges (
       priviligesid bigint PRIMARY KEY DEFAULT nextval('priviliges_priviligesid_no_seq'),
       userid bigint REFERENCES user(userid),
       administrativeRolesid REFERENCES administrativeRoles(administrativeRolesid) ON DELETE CASCADE,
       institutionid bigint REFERENCES institution(institutionid) ON DELETE CASCADE,
       departmentid bigint REFERENCES department(departmentid) ON DELETE CASCADE,
       laboratoryid bigint REFERENCES laboratory(laboratoryid) ON DELETE CASCADE,
       laboratoryInstanceid bigint REFERENCES laboratoryInstance(laboratoryInstanceid) ON DELETE CASCADE
);


DROP TABLE IF EXISTS Numb3rL0ck3r_institution;
CREATE TABLE Numb3rL0ck3r_institution (
       institutionid bigint PRIMARY KEY DEFAULT nextval('institution_institutionid_no_seq'),
       institutionName text,
       institutionDescription text
);

DROP TABLE IF EXISTS Numb3rL0ck3r_department;
CREATE TABLE Numb3rL0ck3r_department (
       departmentid bigint PRIMARY KEY DEFAULT nextval('department_departmentid_no_seq'),
       departmentName text,
       departmentDescription text
);

DROP TABLE IF EXISTS Numb3rL0ck3r_laboratory;
CREATE TABLE Numb3rL0ck3r_laboratory (
       laboratoryid bigint PRIMARY KEY DEFAULT nextval('laboratory_laboratoryid_no_seq'),
       laboratoryName text,
       laboratoryDescription text,
       laboratoryDate timestamp DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS Numb3rL0ck3r_laboratoryInstance;
CREATE TABLE Numb3rL0ck3r_laboratoryInstance (
       laboratoryInstanceid bigint PRIMARY KEY DEFAULT nextval('laboratoryInstance_laboratoryInstanceid_no_seq'),
       laboratoryid bigint REFERENCES laboratory(laboratoryid) ON DELETE CASCADE,
       laboratoryInstanceName text,
       laboratoryInstanceDescription text,
       laboratoryInstanceDate timestamp DEFAULT CURRENT_TIMESTAMP
);


