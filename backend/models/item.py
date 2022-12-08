import mysql.connector
from util.utils import get_user_organisation, get_user_organisation_from_params, get_res

def create_item(request, db_config):
    req = request.get_json()
    organisation_id = get_user_organisation(req, db_config)
    title = req["title"]
    description = req.get("description", None)
    story = req["story"]
    type = req["type"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO item (title, description, story, status, type, sprint, assigned_to)
        VALUES ("{title}", "{description}", {story}, 1, {type}, NULL, NULL);
    ''')
    db.commit()
    lastrowid = cursor.lastrowid
    cursor.close()
    db.close()
    return {"message": "Inserted!", "tuple_id": lastrowid}

def read_items(request, db_config):
    organisation_id = get_user_organisation_from_params(request, db_config)
    story_id = request.args.get("story")
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM item
        WHERE story={story_id};
    ''')
    res = get_res(cursor=cursor)
    db.close()
    return {"items": res}

def update_item(request, db_config):
    req = request.get_json()
    organisation_id = get_user_organisation(req, db_config)
    item_id = req["item"]
    title = req["title"]
    description = req.get("description", None)
    story = req["story"]
    status = req["status"]
    type = req["type"]
    sprint = req.get("sprint", "NULL")
    if not sprint:
        sprint = "NULL"
    assigned_to = req.get("assigned_to", "NULL")
    if not assigned_to:
        assigned_to = "NULL"
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        UPDATE item
        SET title="{title}", description="{description}", story={story}, status={status}, type={type}, sprint={sprint}, assigned_to={assigned_to}
        WHERE id={item_id};
    ''')
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Updated!"}

def delete_item(request, db_config):
    req = request.get_json()
    organisation_id = get_user_organisation(req, db_config)
    item_id = req["item"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        DELETE FROM item
        WHERE id={item_id};
    ''')
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Deleted!"}