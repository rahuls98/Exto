import mysql.connector
from util.utils import get_admin_organisation, get_user_organisation_from_params, get_res

def create_customer(request, db_config):
    req = request.get_json()
    organisation_id = get_admin_organisation(req, db_config)
    name = req["name"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO customer (name, organisation)
        VALUES ("{name}", {organisation_id});
    ''')
    db.commit()
    lastrowid = cursor.lastrowid
    cursor.close()
    db.close()
    return {"message": "Inserted!", "tuple_id": lastrowid}


def read_customers(request, db_config):
    organisation_id = get_user_organisation_from_params(request, db_config)
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM customer
        WHERE organisation={organisation_id};
    ''')
    res = get_res(cursor=cursor)
    db.close()
    return {"customers": res}


def update_customer(request, db_config):
    req = request.get_json()
    organisation_id = get_admin_organisation(req, db_config)
    customer_id = req["customer"]
    name = req["name"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        UPDATE customer
        SET name="{name}"
        WHERE organisation={organisation_id} AND id={customer_id};
    ''')
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Updated!"}


def delete_customer(request, db_config):
    req = request.get_json()
    organisation_id = get_admin_organisation(req, db_config)
    customer_id = req["customer"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        DELETE FROM customer
        WHERE organisation={organisation_id} AND id={customer_id};
    ''')
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Deleted!"}
