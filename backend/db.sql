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
    completed BOOLEAN NOT NULL,
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

DELIMITER //
CREATE PROCEDURE IF NOT EXISTS get_backlog_items(IN organisation_id INTEGER)
BEGIN
	SELECT item.id, item.title
    FROM item JOIN story ON item.story=story.id 
    JOIN project ON story.project=project.id
    WHERE project.organisation=organisation_id AND item.status=1;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE IF NOT EXISTS get_sprint_item_composition(IN sprint_id INTEGER)
BEGIN
	SELECT item_status.title AS title, COUNT(*) AS items
    FROM item JOIN item_status ON item.status=item_status.id
    WHERE item.sprint=sprint_id
    GROUP BY item_status.title;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER incomplete_tasks_to_backlog
AFTER UPDATE ON sprint
FOR EACH ROW
BEGIN
    IF OLD.completed=FALSE AND NEW.completed=TRUE THEN
        UPDATE item
        SET status=1, sprint=NULL
        WHERE sprint = NEW.id AND status != 4;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE FUNCTION get_employee_name(
	employee_id INTEGER
) 
RETURNS VARCHAR(200)
DETERMINISTIC
BEGIN
	DECLARE full_name VARCHAR(200);
    
	SELECT CONCAT(first_name, ' ', last_name) 
    FROM employee WHERE id=employee_id
    INTO full_name;
    
    RETURN full_name;
END //
DELIMITER ;

INSERT INTO organisation (name, admin_username, admin_password, user_username, user_password) 
VALUES ("Nike", "admin@nike.com", "admin@nike.com", "user@nike.com", "user@nike.com");

INSERT INTO organisation (name, admin_username, admin_password, user_username, user_password) 
VALUES ("Puma", "admin@puma.com", "admin@puma.com", "user@puma.com", "user@puma.com");

INSERT INTO employee (email, organisation, first_name, last_name)
VALUES ("alice.d@nike.com", 1, "Alice", "D");

INSERT INTO employee (email, organisation, first_name, last_name)
VALUES ("bob.t@nike.com", 1, "Bob", "T");

INSERT INTO employee (email, organisation, first_name, last_name)
VALUES ("charlie.p@nike.com", 1, "Charlie", "P");

INSERT INTO employee (email, organisation, first_name, last_name)
VALUES ("dave.s@nike.com", 1, "Dave", "S");

INSERT INTO developer (id, domain)
VALUES (1, "Web developer");

INSERT INTO tester (id, domain)
VALUES (2, "QA");

INSERT INTO project_manager (id)
VALUES (3);

INSERT INTO scrum_master (id)
VALUES (4);

INSERT INTO customer (name, organisation)
VALUES ("FC Barcelona", 1);

INSERT INTO customer (name, organisation)
VALUES ("Real Madrid", 2);

INSERT INTO item_status (title, tag_color)
VALUES ("Backlog", "grey"), ("Todo", "red"), ("In progress", "yellow"), ("Complete", "green");

INSERT INTO item_type (title, tag_color)
VALUES ("Task", "blue"), ("Bug", "orange"), ("Test", "purple");
