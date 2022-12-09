import mysql.connector
import json
from flask import Response
from util.utils import get_user_organisation, get_user_organisation_from_params, get_res

def create_item(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        req = request.get_json()
        organisation_id = get_user_organisation(req, db_config)
        title = req["title"]
        description = req.get("description", None)
        story = req["story"]
        type = req["type"]
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
        cursor.close()
        db.close()
        res = {"error": str(e.__class__.__name__), "message": str(e)}
        if (str(e.__class__.__name__) == "IntegrityError"):
            res["message"] = "Another item in this story has the same title. Try again!"
        return Response(json.dumps(res), status=400, mimetype='application/json')

def read_items(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        organisation_id = get_user_organisation_from_params(request, db_config)
        story_id = request.args.get("story")
        cursor.execute(f'''
            SELECT *
            FROM item
            WHERE story={story_id};
        ''')
        res = get_res(cursor=cursor)
        db.close()
        return {"items": res}
    except Exception as e:
        db.close()
        return {"error": str(e.__class__.__name__), "message": str(e)}

def read_backlog_items(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        organisation_id = get_user_organisation_from_params(request, db_config)
        cursor.execute(f'''
            CALL get_backlog_items({organisation_id});
        ''')
        res = get_res(cursor=cursor)
        db.close()
        return {"backlog_items": res}
    except Exception as e:
        db.close()
        return {"error": str(e.__class__.__name__), "message": str(e)}

def update_item(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
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
        cursor.close()
        db.close()
        return {"error": str(e.__class__.__name__), "message": str(e)}

def delete_item(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        req = request.get_json()
        organisation_id = get_user_organisation(req, db_config)
        item_id = req["item"]
        cursor.execute(f'''
            DELETE FROM item
            WHERE id={item_id};
        ''')
        db.commit()
        cursor.close()
        db.close()
        return {"message": "Deleted!"}
    except Exception as e:
        cursor.close()
        db.close()
        return {"error": str(e.__class__.__name__), "message": str(e)}