import mysql.connector
import json
from flask import Response
from util.utils import get_user_organisation, get_user_organisation_from_params, get_res

def create_story(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        req = request.get_json()
        organisation_id = get_user_organisation(req, db_config)
        title = req["title"]
        description = req.get("description", None)
        project= req["project"]
        cursor.execute(f'''
            INSERT INTO story (title, description, project)
            VALUES ("{title}", "{description}", {project});
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
            res["message"] = "Another story in this project has the same title. Try again!"
        return Response(json.dumps(res), status=400, mimetype='application/json')

def read_stories(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        organisation_id = get_user_organisation_from_params(request, db_config)
        project_id = request.args.get("project")
        cursor.execute(f'''
            SELECT story.id, story.title, story.description, project.title AS project 
            FROM story JOIN project ON story.project=project.id
            WHERE project.id={project_id};
        ''')
        res = get_res(cursor=cursor)
        db.close()
        return {"stories": res}
    except Exception as e:
        db.close()
        return {"error": str(e.__class__.__name__), "message": str(e)}

def update_story(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        req = request.get_json()
        organisation_id = get_user_organisation(req, db_config)
        story_id = req["story"]
        title = req["title"]
        description = req.get("description", None)
        project = req["project"]
        cursor.execute(f'''
            UPDATE story
            SET title="{title}", description="{description}", project={project}"
            WHERE id={story_id};
        ''')
        db.commit()
        cursor.close()
        db.close()
        return {"message": "Updated!"}
    except Exception as e:
        cursor.close()
        db.close()
        return {"error": str(e.__class__.__name__), "message": str(e)}

def delete_story(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        req = request.get_json()
        organisation_id = get_user_organisation(req, db_config)
        story_id = req["story"]
        cursor.execute(f'''
            DELETE FROM story
            WHERE id={story_id};
        ''')
        db.commit()
        cursor.close()
        db.close()
        return {"message": "Deleted!"}
    except Exception as e:
        cursor.close()
        db.close()
        return {"error": str(e.__class__.__name__), "message": str(e)}