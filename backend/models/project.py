import mysql.connector
from util.utils import get_user_organisation, get_user_organisation_from_params, get_res

def create_project(request, db_config):
    req = request.get_json()
    organisation_id = get_user_organisation(req, db_config)
    title = req["title"]
    customer = req["customer"]
    start_date = req["start_date"]
    end_date = req["end_date"]
    project_manager = req["project_manager"]
    scrum_master = req["scrum_master"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO project (title, organisation, customer, start_date, end_date, project_manager, scrum_master)
        VALUES ("{title}", {organisation_id}, {customer}, "{start_date}", "{end_date}", {project_manager}, {scrum_master});
    ''')
    db.commit()
    lastrowid = cursor.lastrowid
    cursor.close()
    db.close()
    return {"message": "Inserted!", "tuple_id": lastrowid}

def read_projects(request, db_config):
    organisation_id = get_user_organisation_from_params(request, db_config)
    request.args.get('username')
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM project
        WHERE organisation={organisation_id};
    ''')
    res = get_res(cursor=cursor)
    db.close()
    return {"projects": res}

def update_project(request, db_config):
    req = request.get_json()
    organisation_id = get_user_organisation(req, db_config)
    project_id = req["project"]
    title = req["title"]
    customer = req["customer"]
    start_date = req["start_date"]
    end_date = req["end_date"]
    project_manager = req["project_manager"]
    scrum_master = req["scrum_master"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        UPDATE project
        SET title="{title}", customer={customer}, start_date="{start_date}", end_date="{end_date}", project_manager={project_manager}, scrum_master={scrum_master}
        WHERE organisation={organisation_id} AND id={project_id};
    ''')
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Updated!"}

def delete_project(request, db_config):
    # organisation_id = get_user_organisation_from_params(request, db_config)
    # project_id = request.args.get('project')
    req = request.get_json()
    organisation_id = get_user_organisation(req, db_config)
    project_id = req["project"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        DELETE FROM project
        WHERE organisation={organisation_id} AND id={project_id};
    ''')
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Deleted!"}