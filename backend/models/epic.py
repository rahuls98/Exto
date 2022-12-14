import mysql.connector
from util.utils import get_user_organisation, get_user_organisation_from_params, get_res

def create_epic(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        req = request.get_json()
        organisation_id = get_user_organisation(req, db_config)
        title = req["title"]
        description = req.get("description", )
        project = req["project"]
        cursor.execute(f'''
            INSERT INTO epic (title, description, project)
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
        return {"error": str(e.__class__.__name__), "message": str(e)}

def read_epics(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        organisation_id = get_user_organisation_from_params(request, db_config)
        project_id = request.args.get("project")
        cursor.execute(f'''
            SELECT *
            FROM epic
            WHERE project={project_id};
        ''')
        res = get_res(cursor=cursor)
        db.close()
        return {"epics": res}
    except Exception as e:
        db.close()
        return {"error": str(e.__class__.__name__), "message": str(e)}

def update_epic(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        req = request.get_json()
        organisation_id = get_user_organisation(req, db_config)
        epic_id = req["epic"]
        title = req["title"]
        description = req.get("description", )
        project = req["project"]
        cursor.execute(f'''
            UPDATE epic
            SET title="{title}", description="{description}", project={project}
            WHERE id={epic_id};
        ''')
        db.commit()
        cursor.close()
        db.close()
        return {"message": "Updated!"}
    except Exception as e:
        cursor.close()
        db.close()
        return {"error": str(e.__class__.__name__), "message": str(e)}

def delete_epic(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        req = request.get_json()
        organisation_id = get_user_organisation(req, db_config)
        epic_id = req["epic"]
        cursor.execute(f'''
            DELETE FROM epic
            WHERE id={epic_id};
        ''')
        db.commit()
        cursor.close()
        db.close()
        return {"message": "Deleted!"}
    except Exception as e:
        cursor.close()
        db.close()
        return {"error": str(e.__class__.__name__), "message": str(e)}