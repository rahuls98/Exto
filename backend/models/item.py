import mysql.connector
from util.utils import get_user_organisation, get_user_organisation_from_params, get_res

def create_item(request, db_config):
    try:
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
    except Exception as e:
        return {"error": e.__class__.__name__, "message": e}

def read_items(request, db_config):
    try:
        organisation_id = get_user_organisation_from_params(request, db_config)
        story_id = request.args.get("story")
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute(f'''
            SELECT item.title, CONCAT(employee.first_name, ' ', employee.last_name) AS assigned_to, item.sprint, item.type, item.status
            FROM item join employee on item.assigned_to=employee.id
            WHERE story={story_id};
        ''')
        res = get_res(cursor=cursor)
        db.close()
        return {"items": res}
    except Exception as e:
        return {"error": e.__class__.__name__, "message": e}

def read_backlog_items(request, db_config):
    try:
        organisation_id = get_user_organisation_from_params(request, db_config)
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute(f'''
            CALL get_backlog_items({organisation_id});
        ''')
        res = get_res(cursor=cursor)
        db.close()
        return {"backlog_items": res}
    except Exception as e:
        return {"error": e.__class__.__name__, "message": e}

def update_item(request, db_config):
    try:
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
    except Exception as e:
        return {"error": e.__class__.__name__, "message": e}

def delete_item(request, db_config):
    try:
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
    except Exception as e:
        return {"error": e.__class__.__name__, "message": e}