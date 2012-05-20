

-- create the schemas to use
CREATE SCHEMA admin;
CREATE SCHEMA laboratory;
CREATE SCHEMA userInfo;
CREATE SCHEMA siteInfo;

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
       administrativeRolesPassPhrase text,
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


DROP TABLE IF EXISTS siteInfo.genericVariables;
CREATE TABLE siteInfo.genericVariables (
       genericVariablesID SERIAL,
       variableName TEXT NOT NULL,
       variableValue TEXT NOT NULL,
       variableDescription TEXT NOT NULL,
       PRIMARY KEY (genericVariablesID)
);


INSERT INTO genericVariables (genericVariablesID, variableName, variableValue, variableDescription) VALUES (1,'ROOTURL','http://black.sc.clarkson.edu/cgi-bin/','The base URL. All URLs <br> will start with this. (Should end in a /)\r\n\r\n\r\n\r\n\r\n');
INSERT INTO genericVariables (genericVariablesID, variableName, variableValue, variableDescription) VALUES (2,'TEXTDIR','/','The directory where static <br> files are kept.\r\n\r\n\r\n\r\n\r\n\r\n');
INSERT INTO genericVariables (genericVariablesID, variableName, variableValue, variableDescription) VALUES (3,'IMAGEDIR','/image/','The directory where images <br> are kept.\r\n\r\n\r\n\r\n\r\n\r\n');
INSERT INTO genericVariables (genericVariablesID, variableName, variableValue, variableDescription) VALUES (4,'LOGINURL','login.cgi','The name of the file used <br> for logins.\r\n\r\n\r\n\r\n\r\n\r\n');
INSERT INTO genericVariables (genericVariablesID, variableName, variableValue, variableDescription) VALUES (5,'LOGOUTURL','logout.cgi','The name of the file used <br> for logouts.\r\n\r\n\r\n\r\n\r\n\r\n');
INSERT INTO genericVariables (genericVariablesID, variableName, variableValue, variableDescription) VALUES (6,'COOKIEDOMAIN','black.sc.clarkson.edu','The domain name for cookies.\r\n\r\n\r\n\r\n\r\n\r\n');
INSERT INTO genericVariables (genericVariablesID, variableName, variableValue, variableDescription) VALUES (7,'COOKIEPATH','/cgi-bin','The path used for cookies.\r\n\r\n\r\n\r\n\r\n\r\n');
INSERT INTO genericVariables (genericVariablesID, variableName, variableValue, variableDescription) VALUES (8,'FAQURL','faq.html','The name of the file used <br> to generate the FAQ.\r\n\r\n\r\n\r\n\r\n\r\n');
INSERT INTO genericVariables (genericVariablesID, variableName, variableValue, variableDescription) VALUES (9,'FROMEMAIL','webmaster@black.sc.clarkson.edu','Email address that emails <br> should appear to be from.\r\n\r\n\r\n\r\n\r\n\r\n');
INSERT INTO genericVariables (genericVariablesID, variableName, variableValue, variableDescription) VALUES (10,'SENDMAIL','/usr/sbin/sendmail','The name of the command <br> to call to send email.\r\n\r\n\r\n\r\n\r\n\r\n');
INSERT INTO genericVariables (genericVariablesID, variableName, variableValue, variableDescription) VALUES (11,'ADMINMAIL','webmaster@black.sc.clarkson.edu','The email address for the <br> site administrator.\r\n\r\n\r\n\r\n\r\n\r\n');

INSERT INTO genericVariables (genericVariablesID, variableName, variableValue, variableDescription) VALUES (12,'public captcha','6LcllQQAAAAAABDGCYzQqTL933odVQvOa8_ja71t','Public re-captcha key.\r\n');
INSERT INTO genericVariables (genericVariablesID, variableName, variableValue, variableDescription) VALUES (13,'private captcha','6LcllQQAAAAAAOm26V4raBtzx6Ae9fjQdktGaOTo','Private captcha key.\r\n');



DROP TABLE IF EXISTS siteInfo.template;
CREATE TABLE siteInfo.template (
       templateID SERIAL,
       templateFile TEXT NOT NULL,
       action TEXT,
       stage TEXT,
       PRIMARY KEY (templateID)
);


-- select tablename from pg_tables where tablename  ~ '^numb+';



