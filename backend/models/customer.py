import mysql.connector
from util.utils import get_admin_organisation, get_user_organisation_from_params, get_res

def create_customer(request, db_config):
    try:
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
    except Exception as e:
        return {"error": str(e.__class__.__name__), "message": str(e)}


def read_customers(request, db_config):
    try:
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
    except Exception as e:
        return {"error": str(e.__class__.__name__), "message": str(e)}


def update_customer(request, db_config):
    try:
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
    except Exception as e:
        return {"error": str(e.__class__.__name__), "message": str(e)}


def delete_customer(request, db_config):
    try:
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
    except Exception as e:
        return {"error": str(e.__class__.__name__), "message": str(e)}
