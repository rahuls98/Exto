import mysql.connector
from util.utils import get_admin_organisation, get_user_organisation_from_params, get_res

def create_scrummaster(request, db_config):
    req = request.get_json()
    organisation_id = get_admin_organisation(req, db_config)
    employee_id = req["employee"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO scrum_master (id)
        VALUES ({employee_id});
    ''')
    db.commit()
    lastrowid = cursor.lastrowid
    cursor.close()
    db.close()
    return {"message": "Inserted!", "tuple_id": lastrowid}

def read_scrummasters(request, db_config):
    organisation_id = get_user_organisation_from_params(request, db_config)
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT employee.id AS id, employee.first_name as first_name, employee.last_name as last_name
        FROM employee JOIN scrum_master ON employee.id=scrum_master.id
        WHERE organisation={organisation_id};
    ''')
    res = get_res(cursor=cursor)
    db.close()
    return {"scrum_masters": res}