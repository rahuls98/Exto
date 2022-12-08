import mysql.connector
from util.utils import get_user_organisation, get_user_organisation_from_params, get_res

def create_sprint(request, db_config):
    req = request.get_json()
    organisation_id = get_user_organisation(req, db_config)
    sprint_number = req["sprint_number"]
    start_date = req["start_date"]
    duration = req["duration"]
    definition_of_done = req.get("definition_of_done", None)
    project = req["project"]
    scrum_master = req["scrum_master"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO sprint (sprint_number, start_date, duration, definition_of_done, project, scrum_master)
        VALUES ({sprint_number}, "{start_date}", {duration}, "{definition_of_done}", {project}, {scrum_master});
    ''')
    db.commit()
    lastrowid = cursor.lastrowid
    cursor.close()
    db.close()
    return {"message": "Inserted!", "tuple_id": lastrowid}

def read_sprints(request, db_config):
    organisation_id = get_user_organisation_from_params(request, db_config)
    project_id = request.args.get("project")
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM sprint
        WHERE project={project_id};
    ''')
    res = get_res(cursor=cursor)
    db.close()
    return {"sprints": res}

def update_sprint(request, db_config):
    req = request.get_json()
    organisation_id = get_user_organisation(req, db_config)
    sprint_id = req["sprint"]
    sprint_number = req["sprint_number"]
    start_date = req["start_date"]
    duration = req["duration"]
    definition_of_done = req.get("definition_of_done", None)
    project = req["project"]
    scrum_master = req["scrum_master"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        UPDATE sprint
        SET sprint_number={sprint_number}, start_date="{start_date}", duration={duration}, definition_of_done="{definition_of_done}", project={project}, scrum_master={scrum_master}
        WHERE id={sprint_id};
    ''')
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Updated!"}

def delete_sprint(request, db_config):
    req = request.get_json()
    organisation_id = get_user_organisation(req)
    sprint_id = req["sprint"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        DELETE FROM sprint
        WHERE id={sprint_id};
    ''')
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Deleted!"}