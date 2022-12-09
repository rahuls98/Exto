import mysql.connector
from util.utils import get_admin_organisation, get_user_organisation_from_params, get_res

def create_employee(request, db_config):
    try:
        req = request.get_json()
        organisation_id = get_admin_organisation(req, db_config)
        email = req["email"]
        first_name = req["first_name"]
        last_name = req["last_name"]
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute(f'''
            INSERT INTO employee (email, organisation, first_name, last_name)
            VALUES ("{email}", {organisation_id}, "{first_name}", "{last_name}");
        ''')
        db.commit()
        lastrowid = cursor.lastrowid
        cursor.close()
        db.close()
        return {"message": "Inserted!", "tuple_id": lastrowid}
    except Exception as e:
        return {"error": e.__class__.__name__, "message": e}

def read_employees(request, db_config):
    try:
        organisation_id = get_user_organisation_from_params(request, db_config)
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute(f'''
            SELECT *
            FROM employee
            WHERE organisation={organisation_id};
        ''')
        res = get_res(cursor=cursor)
        db.close()
        return {"employees": res}
    except Exception as e:
        return {"error": e.__class__.__name__, "message": e}

def read_employee_name(request, db_config):
    try:
        organisation_id = get_user_organisation_from_params(request, db_config)
        employee_id = request.args.get('employee')
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute(f'''
            SELECT get_employee_name({employee_id});
        ''')
        full_name = cursor.fetchone()[0]
        db.close()
        return {"full_name": full_name}
    except Exception as e:
        return {"error": e.__class__.__name__, "message": e}

def update_employee(request, db_config):
    try:
        req = request.get_json()
        organisation_id = get_admin_organisation(req, db_config)
        employee_id = req["employee"]
        email = req["email"]
        first_name = req["first_name"]
        last_name = req["last_name"]
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute(f'''
            UPDATE employee
            SET email="{email}", first_name="{first_name}", last_name="{last_name}"
            WHERE organisation={organisation_id} AND id={employee_id};
        ''')
        db.commit()
        cursor.close()
        db.close()
        return {"message": "Updated!"}
    except Exception as e:
        return {"error": e.__class__.__name__, "message": e}

def delete_employee(request, db_config):
    try:
        req = request.get_json()
        organisation_id = get_admin_organisation(req, db_config)
        employee_id = req["employee"]
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute(f'''
            DELETE FROM employee
            WHERE organisation={organisation_id} AND id={employee_id};
        ''')
        db.commit()
        cursor.close()
        db.close()
        return {"message": "Deleted!"}
    except Exception as e:
        return {"error": e.__class__.__name__, "message": e}