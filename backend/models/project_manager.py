import mysql.connector
from util.utils import get_admin_organisation, get_user_organisation_from_params, get_res

def create_projectmanager(request, db_config):
    req = request.get_json()
    organisation_id = get_admin_organisation(req, db_config)
    employee_id = req["employee"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO project_manager (id)
        VALUES ({employee_id});
    ''')
    db.commit()
    cursor.lastrowid = cursor.lastrowid
    cursor.close()
    db.close()
    return {"message": "Inserted!", "tuple_id": lastrowid}

def read_projectmanagers(request, db_config):
    organisation_id = get_user_organisation_from_params(request, db_config)
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM employee JOIN project_manager ON employee.id=project_manager.id
        WHERE organisation={organisation_id};
    ''')
    res = get_res(cursor=cursor)
    db.close()
    return {"project_managers": res}