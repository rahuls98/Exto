import json
from flask import Flask, request
from flask_cors import CORS
import mysql.connector

db = None

app = Flask(__name__)
CORS(app)

def get_admin_organisation(req):
    username = req["admin_username"]
    password = req["admin_password"]
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT id 
        FROM organisation 
        WHERE admin_username="{username}" AND admin_password="{password}";
    ''')
    organisation_id = cursor.fetchone()[0]
    cursor.close()
    return organisation_id

def get_user_organisation(req):
    username = req["user_username"]
    password = req["user_password"]
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT id 
        FROM organisation 
        WHERE user_username="{username}" AND user_password="{password}";
    ''')
    organisation_id = cursor.fetchone()[0]
    cursor.close()
    return organisation_id

def get_user_organisation_from_params(req):
    username = req.args.get("user_username")
    password = req.args.get("user_password")
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT id 
        FROM organisation 
        WHERE user_username="{username}" AND user_password="{password}";
    ''')
    organisation_id = cursor.fetchone()[0]
    cursor.close()
    return organisation_id

def get_res(cursor):
    tuples = cursor.fetchall() 
    descriptions = cursor.description
    cursor.close()
    res = []
    for tuple in tuples:
        details = {}
        for i in range(len(descriptions)):
            details[descriptions[i][0]] = tuple[i]
        res.append(details)
    return res

#--- Customer ---#
@app.route('/customers', methods = ['POST'])
def create_customer():
    req = request.get_json()
    organisation_id = get_admin_organisation(req)
    name = req["name"]
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO customer (name, organisation)
        VALUES ("{name}", {organisation_id});
    ''')
    db.commit()
    cursor.close()
    return {"message": "Inserted!", "tuple_id": cursor.lastrowid}

@app.route('/customers', methods = ['GET'])
def read_customers():
    organisation_id = get_user_organisation_from_params(request)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM customer
        WHERE organisation={organisation_id};
    ''')
    return {"customers": get_res(cursor=cursor)}

@app.route('/customers', methods = ['PUT'])
def update_customer():
    req = request.get_json()
    organisation_id = get_admin_organisation(req)
    customer_id = req["customer"]
    name = req["name"]
    cursor = db.cursor()
    cursor.execute(f'''
        UPDATE customer
        SET name="{name}"
        WHERE organisation={organisation_id} AND id={customer_id};
    ''')
    db.commit()
    cursor.close()
    return {"message": "Updated!"}

@app.route('/customers', methods = ['DELETE'])
def delete_customer():
    req = request.get_json()
    organisation_id = get_admin_organisation(req)
    customer_id = req["customer"]
    cursor = db.cursor()
    cursor.execute(f'''
        DELETE FROM customer
        WHERE organisation={organisation_id} AND id={customer_id};
    ''')
    db.commit()
    cursor.close()
    return {"message": "Deleted!"}


#--- Employee ---#
@app.route('/employees', methods = ['POST'])
def create_employee():
    req = request.get_json()
    organisation_id = get_admin_organisation(req)
    email = req["email"]
    first_name = req["first_name"]
    last_name = req["last_name"]
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO employee (email, organisation, first_name, last_name)
        VALUES ("{email}", {organisation_id}, "{first_name}", "{last_name}");
    ''')
    db.commit()
    cursor.close()
    return {"message": "Inserted!", "tuple_id": cursor.lastrowid}

@app.route('/employees', methods = ['GET'])
def read_employees():
    organisation_id = get_user_organisation_from_params(request)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM employee
        WHERE organisation={organisation_id};
    ''')
    return {"employees": get_res(cursor=cursor)}

@app.route('/employees', methods = ['PUT'])
def update_employee():
    req = request.get_json()
    organisation_id = get_admin_organisation(req)
    employee_id = req["employee"]
    email = req["email"]
    first_name = req["first_name"]
    last_name = req["last_name"]
    cursor = db.cursor()
    cursor.execute(f'''
        UPDATE employee
        SET email="{email}", first_name="{first_name}", last_name="{last_name}"
        WHERE organisation={organisation_id} AND id={employee_id};
    ''')
    db.commit()
    cursor.close()
    return {"message": "Updated!"}

@app.route('/employee', methods = ['DELETE'])
def delete_employee():
    req = request.get_json()
    organisation_id = get_admin_organisation(req)
    employee_id = req["employee"]
    cursor = db.cursor()
    cursor.execute(f'''
        DELETE FROM employee
        WHERE organisation={organisation_id} AND id={employee_id};
    ''')
    db.commit()
    cursor.close()
    return {"message": "Deleted!"}


#--- Tester ---#
@app.route('/testers', methods = ['POST'])
def create_tester():
    req = request.get_json()
    organisation_id = get_admin_organisation(req)
    employee_id = req["employee"]
    domain = req["domain"]
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO tester (id, domain)
        VALUES ({employee_id}, "{domain}");
    ''')
    db.commit()
    cursor.close()
    return {"message": "Inserted!", "tuple_id": cursor.lastrowid}

@app.route('/testers', methods = ['GET'])
def read_testers():
    organisation_id = get_user_organisation_from_params(request)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM employee JOIN tester ON employee.id=tester.id
        WHERE organisation={organisation_id};
    ''')
    return {"testers": get_res(cursor=cursor)}

@app.route('/testers', methods = ['PUT'])
def update_tester():
    req = request.get_json()
    organisation_id = get_admin_organisation(req)
    cursor = db.cursor()
    tester_id = req["tester"]
    domain = req["domain"]
    cursor.execute(f'''
        UPDATE tester
        SET domain="{domain}"
        WHERE id={tester_id};
    ''')
    db.commit()
    cursor.close()
    return {"message": "Updated!"}


#--- Developer ---#
@app.route('/developers', methods = ['POST'])
def create_developer():
    req = request.get_json()
    organisation_id = get_admin_organisation(req)
    employee_id = req["employee"]
    domain = req["domain"]
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO developer (id, domain)
        VALUES ({employee_id}, "{domain}");
    ''')
    db.commit()
    cursor.close()
    return {"message": "Inserted!", "tuple_id": cursor.lastrowid}

@app.route('/developers', methods = ['GET'])
def read_developers():
    organisation_id = get_user_organisation_from_params(request)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM employee JOIN developer ON employee.id=developer.id
        WHERE organisation={organisation_id};
    ''')
    return {"developers": get_res(cursor=cursor)}

@app.route('/developers', methods = ['PUT'])
def update_developer():
    req = request.get_json()
    organisation_id = get_admin_organisation(req)
    cursor = db.cursor()
    developer_id = req["developer"]
    domain = req["domain"]
    cursor.execute(f'''
        UPDATE developer
        SET domain="{domain}"
        WHERE id={developer_id};
    ''')
    db.commit()
    cursor.close()
    return {"message": "Updated!"}


#--- Scrum master ---#
@app.route('/scrum_masters', methods = ['POST'])
def create_scrummaster():
    req = request.get_json()
    organisation_id = get_admin_organisation(req)
    employee_id = req["employee"]
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO scrum_master (id)
        VALUES ({employee_id});
    ''')
    db.commit()
    cursor.close()
    return {"message": "Inserted!", "tuple_id": cursor.lastrowid}

@app.route('/scrum_masters', methods = ['GET'])
def read_scrummasters():
    organisation_id = get_user_organisation_from_params(request)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM employee JOIN scrum_master ON employee.id=scrum_master.id
        WHERE organisation={organisation_id};
    ''')
    return {"testers": get_res(cursor=cursor)}


#--- Project manager ---#
@app.route('/project_managers', methods = ['POST'])
def create_projectmanager():
    req = request.get_json()
    organisation_id = get_admin_organisation(req)
    employee_id = req["employee"]
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO project_manager (id)
        VALUES ({employee_id});
    ''')
    db.commit()
    cursor.close()
    return {"message": "Inserted!", "tuple_id": cursor.lastrowid}

@app.route('/project_managers', methods = ['GET'])
def read_projectmanagers():
    organisation_id = get_user_organisation_from_params(request)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM employee JOIN project_manager ON employee.id=project_manager.id
        WHERE organisation={organisation_id};
    ''')
    return {"testers": get_res(cursor=cursor)}


#--- Project ---#
@app.route('/projects', methods = ['POST'])
def create_project():
    req = request.get_json()
    organisation_id = get_user_organisation(req)
    title = req["title"]
    customer = req["customer"]
    start_date = req["start_date"]
    end_date = req["end_date"]
    project_manager = req["project_manager"]
    scrum_master = req["scrum_master"]
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO project (title, organisation, customer, start_date, end_date, project_manager, scrum_master)
        VALUES ("{title}", {organisation_id}, {customer}, "{start_date}", "{end_date}", {project_manager}, {scrum_master});
    ''')
    db.commit()
    cursor.close()
    return {"message": "Inserted!", "tuple_id": cursor.lastrowid}

@app.route('/projects', methods = ['GET'])
def read_projects():
    organisation_id = get_user_organisation_from_params(request)
    request.args.get('username')
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM project
        WHERE organisation={organisation_id};
    ''')
    return {"projects": get_res(cursor=cursor)}

@app.route('/projects', methods = ['PUT'])
def update_project():
    req = request.get_json()
    organisation_id = get_user_organisation(req)
    project_id = req["project"]
    title = req["title"]
    customer = req["customer"]
    start_date = req["start_date"]
    end_date = req["end_date"]
    project_manager = req["project_manager"]
    scrum_master = req["scrum_master"]
    cursor = db.cursor()
    cursor.execute(f'''
        UPDATE project
        SET title="{title}", customer={customer}, start_date="{start_date}", end_date="{end_date}", project_manager={project_manager}, scrum_master={scrum_master}
        WHERE organisation={organisation_id} AND id={project_id};
    ''')
    db.commit()
    cursor.close()
    return {"message": "Updated!"}

@app.route('/projects', methods = ['DELETE'])
def delete_project():
    req = request.get_json()
    organisation_id = get_user_organisation(req)
    project_id = req["project"]
    cursor = db.cursor()
    cursor.execute(f'''
        DELETE FROM project
        WHERE organisation={organisation_id} AND id={project_id};
    ''')
    db.commit()
    cursor.close()
    return {"message": "Deleted!"}


#--- Epic ---#
@app.route('/epics', methods = ['POST'])
def create_epics():
    req = request.get_json()
    organisation_id = get_user_organisation(req)
    title = req["title"]
    description = req.get("description", )
    project = req["project"]
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO epic (title, description, project)
        VALUES ("{title}", "{description}", {project});
    ''')
    db.commit()
    cursor.close()
    return {"message": "Inserted!", "tuple_id": cursor.lastrowid}

@app.route('/epics', methods = ['GET'])
def read_epics():
    organisation_id = get_user_organisation_from_params(request)
    project_id = request.args.get("project")
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM epic
        WHERE project={project_id};
    ''')
    return {"epics": get_res(cursor=cursor)}

@app.route('/epics', methods = ['PUT'])
def update_epics():
    req = request.get_json()
    organisation_id = get_user_organisation(req)
    epic_id = req["epic"]
    title = req["title"]
    description = req.get("description", )
    project = req["project"]
    cursor = db.cursor()
    cursor.execute(f'''
        UPDATE epic
        SET title="{title}", description="{description}", project={project}
        WHERE id={epic_id};
    ''')
    db.commit()
    cursor.close()
    return {"message": "Updated!"}

@app.route('/epics', methods = ['DELETE'])
def delete_epics():
    req = request.get_json()
    organisation_id = get_user_organisation(req)
    epic_id = req["epic"]
    cursor = db.cursor()
    cursor.execute(f'''
        DELETE FROM epic
        WHERE id={epic_id};
    ''')
    db.commit()
    cursor.close()
    return {"message": "Deleted!"}


#--- Story ---#
@app.route('/stories', methods = ['POST'])
def create_stories():
    req = request.get_json()
    organisation_id = get_user_organisation(req)
    title = req["title"]
    description = req.get("description", None)
    epic = req["epic"]
    tag_color = req["tag_color"]
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO story (title, description, epic, tag_color)
        VALUES ("{title}", "{description}", {epic}, "{tag_color}");
    ''')
    db.commit()
    cursor.close()
    return {"message": "Inserted!", "tuple_id": cursor.lastrowid}

@app.route('/stories', methods = ['GET'])
def read_stories():
    organisation_id = get_user_organisation_from_params(request)
    epic_id = request.args.get("epic")
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM story
        WHERE epic={epic_id};
    ''')
    return {"stories": get_res(cursor=cursor)}

@app.route('/stories', methods = ['PUT'])
def update_stories():
    req = request.get_json()
    organisation_id = get_user_organisation(req)
    story_id = req["story"]
    title = req["title"]
    description = req.get("description", None)
    epic = req["epic"]
    tag_color = req["tag_color"]
    cursor = db.cursor()
    cursor.execute(f'''
        UPDATE story
        SET title="{title}", description="{description}", epic={epic}, tag_color="{tag_color}"
        WHERE id={story_id};
    ''')
    db.commit()
    cursor.close()
    return {"message": "Updated!"}

@app.route('/stories', methods = ['DELETE'])
def delete_stories():
    req = request.get_json()
    organisation_id = get_user_organisation(req)
    story_id = req["story"]
    cursor = db.cursor()
    cursor.execute(f'''
        DELETE FROM story
        WHERE id={story_id};
    ''')
    db.commit()
    cursor.close()
    return {"message": "Deleted!"}


#--- Item ---#
@app.route('/items', methods = ['POST'])
def create_items():
    req = request.get_json()
    organisation_id = get_user_organisation(req)
    title = req["title"]
    description = req.get("description", None)
    story = req["story"]
    type = req["type"]
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO item (title, description, story, status, type, sprint, assigned_to)
        VALUES ("{title}", "{description}", {story}, 1, {type}, NULL, NULL);
    ''')
    db.commit()
    cursor.close()
    return {"message": "Inserted!", "tuple_id": cursor.lastrowid}

@app.route('/items', methods = ['GET'])
def read_items():
    organisation_id = get_user_organisation_from_params(request)
    story_id = request.args.get("story")
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM item
        WHERE story={story_id};
    ''')
    return {"items": get_res(cursor=cursor)}

@app.route('/items', methods = ['PUT'])
def update_items():
    req = request.get_json()
    organisation_id = get_user_organisation(req)
    item_id = req["item"]
    title = req["title"]
    description = req.get("description", None)
    story = req["story"]
    status = req["status"]
    type = req["type"]
    sprint = req.get("sprint", "NULL")
    if not sprint:
        sprint = "NULL"
    assigned_to = req.get("assigned_to", "NULL")
    if not assigned_to:
        assigned_to = "NULL"
    cursor = db.cursor()
    cursor.execute(f'''
        UPDATE item
        SET title="{title}", description="{description}", story={story}, status={status}, type={type}, sprint={sprint}, assigned_to={assigned_to}
        WHERE id={item_id};
    ''')
    db.commit()
    cursor.close()
    return {"message": "Updated!"}

@app.route('/items', methods = ['DELETE'])
def delete_items():
    req = request.get_json()
    organisation_id = get_user_organisation(req)
    item_id = req["item"]
    cursor = db.cursor()
    cursor.execute(f'''
        DELETE FROM item
        WHERE id={item_id};
    ''')
    db.commit()
    cursor.close()
    return {"message": "Deleted!"}


#--- Sprint ---#
@app.route('/sprints', methods = ['POST'])
def create_sprints():
    req = request.get_json()
    organisation_id = get_user_organisation(req)
    sprint_number = req["sprint_number"]
    start_date = req["start_date"]
    duration = req["duration"]
    definition_of_done = req.get("definition_of_done", None)
    project = req["project"]
    scrum_master = req["scrum_master"]
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO sprint (sprint_number, start_date, duration, definition_of_done, project, scrum_master)
        VALUES ({sprint_number}, "{start_date}", {duration}, "{definition_of_done}", {project}, {scrum_master});
    ''')
    db.commit()
    cursor.close()
    return {"message": "Inserted!", "tuple_id": cursor.lastrowid}

@app.route('/sprints', methods = ['GET'])
def read_sprints():
    organisation_id = get_user_organisation_from_params(request)
    project_id = request.args.get("project")
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM sprint
        WHERE project={project_id};
    ''')
    return {"sprints": get_res(cursor=cursor)}

@app.route('/sprints', methods = ['PUT'])
def update_sprints():
    req = request.get_json()
    organisation_id = get_user_organisation(req)
    sprint_id = req["sprint"]
    sprint_number = req["sprint_number"]
    start_date = req["start_date"]
    duration = req["duration"]
    definition_of_done = req.get("definition_of_done", None)
    project = req["project"]
    scrum_master = req["scrum_master"]
    cursor = db.cursor()
    cursor.execute(f'''
        UPDATE sprint
        SET sprint_number={sprint_number}, start_date="{start_date}", duration={duration}, definition_of_done="{definition_of_done}", project={project}, scrum_master={scrum_master}
        WHERE id={sprint_id};
    ''')
    db.commit()
    cursor.close()
    return {"message": "Updated!"}

@app.route('/sprints', methods = ['DELETE'])
def delete_sprints():
    req = request.get_json()
    organisation_id = get_user_organisation(req)
    sprint_id = req["sprint"]
    cursor = db.cursor()
    cursor.execute(f'''
        DELETE FROM sprint
        WHERE id={sprint_id};
    ''')
    db.commit()
    cursor.close()
    return {"message": "Deleted!"}


#--- Item status ---#
@app.route('/item_statuses', methods = ['GET'])
def read_itemstatuses():
    # req = request.get_json()
    # organisation_id = get_user_organisation(req)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM item_status;
    ''')
    return {"item_statuses": get_res(cursor=cursor)}


#--- Item types ---#
@app.route('/item_types', methods = ['GET'])
def read_itemtypes():
    # req = request.get_json()
    # organisation_id = get_user_organisation(req)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM item_type;
    ''')
    return {"item_typees": get_res(cursor=cursor)}


if __name__ == '__main__':
    CONFIG = None
    with open("./config.json", "rb") as f:
        CONFIG = json.load(f)
    db = mysql.connector.connect(
        host=CONFIG["DATABASE"]["HOST"],
        user=CONFIG["DATABASE"]["USER"],
        password=CONFIG["DATABASE"]["PASSWORD"],
        database=CONFIG["DATABASE"]["NAME"]
    )
    app.run(
        host=CONFIG["APPLICATION"]["HOST"],
        port=CONFIG["APPLICATION"]["PORT"], 
        debug=CONFIG["APPLICATION"]["DEBUG"]
    )
    db.close()
