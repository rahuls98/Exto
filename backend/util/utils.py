import mysql.connector

def get_admin_organisation(request, db_config):
    username = request["admin_username"]
    password = request["admin_password"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT id 
        FROM organisation 
        WHERE admin_username="{username}" AND admin_password="{password}";
    ''')
    organisation_id = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return organisation_id


def get_user_organisation(request, db_config):
    username = request["user_username"]
    password = request["user_password"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT id 
        FROM organisation 
        WHERE user_username="{username}" AND user_password="{password}";
    ''')
    organisation_id = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return organisation_id


def get_user_organisation_from_params(request, db_config):
    username = request.args.get("user_username")
    password = request.args.get("user_password")
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT id 
        FROM organisation 
        WHERE user_username="{username}" AND user_password="{password}";
    ''')
    organisation_id = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return organisation_id


def get_res(cursor):
    tuples = cursor.fetchall() 
    descriptions = cursor.description
    cursor.close()
    res = []
    for tuple in tuples:
        details = {}
        for i in range(len(descriptions)):
            details[descriptions[i][0]] = tuple[i]
        res.append(details)
    return res
