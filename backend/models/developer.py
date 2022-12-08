import mysql.connector
from util.utils import get_admin_organisation, get_user_organisation_from_params, get_res

def create_developer(request, db_config):
    req = request.get_json()
    organisation_id = get_admin_organisation(req, db_config)
    employee_id = req["employee"]
    domain = req["domain"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO developer (id, domain)
        VALUES ({employee_id}, "{domain}");
    ''')
    db.commit()
    lastrowid = cursor.lastrowid
    cursor.close()
    db.close()
    return {"message": "Inserted!", "tuple_id": lastrowid}

def read_developers(request, db_config):
    organisation_id = get_user_organisation_from_params(request, db_config)
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM employee JOIN developer ON employee.id=developer.id
        WHERE organisation={organisation_id};
    ''')
    res = get_res(cursor=cursor)
    db.close()
    return {"developers": res}

def update_developer(request, db_config):
    req = request.get_json()
    organisation_id = get_admin_organisation(req, db_config)
    db = mysql.connector.connect(**db_config)
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
    db.close()
    return {"message": "Updated!"}