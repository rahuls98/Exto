CREATE DATABASE IF NOT EXISTS exto;

USE exto;

CREATE TABLE IF NOT EXISTS organisation (
    id INTEGER AUTO_INCREMENT NOT NULL,
    name VARCHAR(100) NOT NULL,
    admin_username VARCHAR(100) NOT NULL,
    admin_password VARCHAR(100) NOT NULL,
    user_username VARCHAR(100) NOT NULL,
    user_password VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT uq_admin_username UNIQUE (admin_username),
    CONSTRAINT uq_user_username UNIQUE (user_username)
);

CREATE TABLE IF NOT EXISTS customer (
    id INTEGER AUTO_INCREMENT NOT NULL,
    name VARCHAR(100) NOT NULL,
    organisation INTEGER NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_customer_organisation FOREIGN KEY (organisation) REFERENCES organisation (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT uq_organisation_customer UNIQUE (organisation, name)
);

CREATE TABLE IF NOT EXISTS employee (
    id INTEGER AUTO_INCREMENT NOT NULL,
    email VARCHAR(100) NOT NULL,
    organisation INTEGER NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_employee_organisation FOREIGN KEY (organisation) REFERENCES organisation (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT uq_employee_email UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS tester (
    id INTEGER NOT NULL,
    domain VARCHAR(100) NOT NULL,
    CONSTRAINT fk_tester_employee FOREIGN KEY (id) REFERENCES employee (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS developer (
    id INTEGER NOT NULL,
    domain VARCHAR(100) NOT NULL,
    CONSTRAINT fk_developer_employee FOREIGN KEY (id) REFERENCES employee (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS scrum_master (
    id INTEGER NOT NULL,
    CONSTRAINT fk_scrummaster_employee FOREIGN KEY (id) REFERENCES employee (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS project_manager (
    id INTEGER NOT NULL,
    CONSTRAINT fk_projectmanager_employee FOREIGN KEY (id) REFERENCES employee (id) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS team (
    id INTEGER AUTO_INCREMENT NOT NULL,
    name VARCHAR(100) NOT NULL,
    organisation INTEGER NOT NULL,
    team_lead INTEGER NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_team_organisation FOREIGN KEY (organisation) REFERENCES organisation (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_team_employee FOREIGN KEY (team_lead) REFERENCES employee (id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT uq_organisation_team UNIQUE (organisation, name)
);

CREATE TABLE IF NOT EXISTS employee_worksin_team (
    employee INTEGER NOT NULL,
    team INTEGER NOT NULL,
    PRIMARY KEY (employee, team),
    CONSTRAINT fk_employeeworksinteam_employee FOREIGN KEY (employee) REFERENCES employee (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_employeeworksinteam_team FOREIGN KEY (team) REFERENCES team (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS project (
    id INTEGER AUTO_INCREMENT NOT NULL,
    title VARCHAR(100) NOT NULL,
    organisation INTEGER NOT NULL,
    customer INTEGER NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    project_manager INTEGER NULL,
    scrum_master INTEGER NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_project_organisation FOREIGN KEY (organisation) REFERENCES organisation (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_project_customer FOREIGN KEY (customer) REFERENCES customer (id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_project_projectmanager FOREIGN KEY (project_manager) REFERENCES project_manager (id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_project_scrummaster FOREIGN KEY (scrum_master) REFERENCES scrum_master (id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT uq_organisation_project UNIQUE (organisation, title)
);

CREATE TABLE IF NOT EXISTS story (
    id INTEGER AUTO_INCREMENT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(500) NULL,
    project INTEGER NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_story_project FOREIGN KEY (project) REFERENCES project (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT uq_project_story UNIQUE (project, title)
);

CREATE TABLE IF NOT EXISTS item_status (
    id INTEGER AUTO_INCREMENT NOT NULL,
    title VARCHAR(30) NOT NULL,
    tag_color VARCHAR(10) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT uq_status_title UNIQUE (title),
    CONSTRAINT uq_status_tagcolor UNIQUE (tag_color)
);

CREATE TABLE IF NOT EXISTS item_type (
    id INTEGER AUTO_INCREMENT NOT NULL,
    title VARCHAR(30) NOT NULL,
    tag_color VARCHAR(10) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT uq_type_title UNIQUE (title),
    CONSTRAINT uq_type_tagcolor UNIQUE (tag_color)
);

CREATE TABLE IF NOT EXISTS sprint (
    id INTEGER AUTO_INCREMENT NOT NULL,
    sprint_number INTEGER NOT NULL,
    start_date DATE NOT NULL,
    duration INTEGER NOT NULL,
    definition_of_done VARCHAR(500) NULL,
    project INTEGER NOT NULL,
    scrum_master INTEGER NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_sprint_project FOREIGN KEY (project) REFERENCES project (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_sprint_scrummaster FOREIGN KEY (scrum_master) REFERENCES scrum_master (id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT uq_project_sprintnumber UNIQUE (project, sprint_number)
);

CREATE TABLE IF NOT EXISTS item (
    id INTEGER AUTO_INCREMENT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(500) NULL,
    story INTEGER NOT NULL,
    status INTEGER NULL,
    type INTEGER NULL,
    sprint INTEGER NULL,
    assigned_to INTEGER NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_item_story FOREIGN KEY (story) REFERENCES story (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_item_status FOREIGN KEY (status) REFERENCES item_status (id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_item_type FOREIGN KEY (type) REFERENCES item_type (id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_item_sprint FOREIGN KEY (sprint) REFERENCES sprint (id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_item_employee FOREIGN KEY (assigned_to) REFERENCES employee (id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT uq_story_item UNIQUE (story, title)
);
