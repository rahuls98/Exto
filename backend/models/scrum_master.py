import mysql.connector
from util.utils import get_admin_organisation, get_user_organisation_from_params, get_res

def create_scrummaster(request, db_config):
    try:
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
    except Exception as e:
        return {"error": str(e.__class__.__name__), "message": str(e)}

def read_scrummasters(request, db_config):
    try:
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
    except Exception as e:
        return {"error": str(e.__class__.__name__), "message": str(e)}