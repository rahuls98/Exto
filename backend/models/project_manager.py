import mysql.connector
from util.utils import get_admin_organisation, get_user_organisation_from_params, get_res

def create_projectmanager(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        req = request.get_json()
        organisation_id = get_admin_organisation(req, db_config)
        employee_id = req["employee"]
        cursor.execute(f'''
            INSERT INTO project_manager (id)
            VALUES ({employee_id});
        ''')
        db.commit()
        lastrowid = cursor.lastrowid
        cursor.close()
        db.close()
        return {"message": "Inserted!", "tuple_id": lastrowid}
    except Exception as e:
        cursor.close()
        db.close()
        return {"error": str(e.__class__.__name__), "message": str(e)}

def read_projectmanagers(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        organisation_id = get_user_organisation_from_params(request, db_config)
        cursor.execute(f'''
            SELECT *
            FROM employee JOIN project_manager ON employee.id=project_manager.id
            WHERE organisation={organisation_id};
        ''')
        res = get_res(cursor=cursor)
        db.close()
        return {"project_managers": res}
    except Exception as e:
        db.close()
        return {"error": str(e.__class__.__name__), "message": str(e)}