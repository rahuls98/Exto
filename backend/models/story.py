import mysql.connector
from util.utils import get_user_organisation, get_user_organisation_from_params, get_res

def create_story(request, db_config):
    req = request.get_json()
    organisation_id = get_user_organisation(req, db_config)
    title = req["title"]
    description = req.get("description", None)
    project= req["project"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        INSERT INTO story (title, description, project)
        VALUES ("{title}", "{description}", {project});
    ''')
    db.commit()
    lastrowid = cursor.lastrowid
    cursor.close()
    db.close()
    return {"message": "Inserted!", "tuple_id": lastrowid}

def read_stories(request, db_config):
    organisation_id = get_user_organisation_from_params(request, db_config)
    project_id = request.args.get("project")
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        SELECT *
        FROM story
        WHERE project={project_id};
    ''')
    res = get_res(cursor=cursor)
    db.close()
    return {"stories": res}

def update_story(request, db_config):
    req = request.get_json()
    organisation_id = get_user_organisation(req, db_config)
    story_id = req["story"]
    title = req["title"]
    description = req.get("description", None)
    project = req["project"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        UPDATE story
        SET title="{title}", description="{description}", project={project}"
        WHERE id={story_id};
    ''')
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Updated!"}

def delete_story(request, db_config):
    req = request.get_json()
    organisation_id = get_user_organisation(req, db_config)
    story_id = req["story"]
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(f'''
        DELETE FROM story
        WHERE id={story_id};
    ''')
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Deleted!"}