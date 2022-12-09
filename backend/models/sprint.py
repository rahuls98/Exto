import mysql.connector
import json
from flask import Response
from util.utils import get_user_organisation, get_user_organisation_from_params, get_res

def create_sprint(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        req = request.get_json()
        organisation_id = get_user_organisation(req, db_config)
        sprint_number = req["sprint_number"]
        start_date = req["start_date"]
        duration = req["duration"]
        definition_of_done = req.get("definition_of_done", None)
        project = req["project"]
        scrum_master = req["scrum_master"]
        items = req["items"]
        items_str = ",".join([str(item) for item in items])
        cursor.execute(f'''
            INSERT INTO sprint (sprint_number, start_date, duration, definition_of_done, project, scrum_master, completed)
            VALUES ({sprint_number}, "{start_date}", {duration}, "{definition_of_done}", {project}, {scrum_master}, False);
        ''')
        lastrowid = cursor.lastrowid
        cursor.execute(f'''
            UPDATE item
            SET sprint={lastrowid}, status={2}
            WHERE id IN ({items_str});
        ''')
        db.commit()
        cursor.close()
        db.close()
        return {"message": "Inserted!", "tuple_id": lastrowid}
    except Exception as e:
        cursor.close()
        db.close()
        res = {"error": str(e.__class__.__name__), "message": str(e)}
        if (str(e.__class__.__name__) == "IntegrityError"):
            res["message"] = "Provided sprint number for this project already exists. Try again!"
        return Response(json.dumps(res), status=400, mimetype='application/json')

def read_sprints(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        organisation_id = get_user_organisation_from_params(request, db_config)
        # project_id = request.args.get("project")
        cursor.execute(f'''
            SELECT sprint.id, project.title AS project, sprint.sprint_number, sprint.start_date, sprint.duration, CONCAT(employee.first_name, ' ', employee.last_name) AS scrum_master, sprint.completed
            FROM sprint JOIN project ON sprint.project=project.id 
            JOIN employee ON sprint.scrum_master=employee.id;
        ''')
        res = get_res(cursor=cursor)
        db.close()
        return {"sprints": res}
    except Exception as e:
        db.close()
        return {"error": str(e.__class__.__name__), "message": str(e)}

def read_item_composition(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        organisation_id = get_user_organisation_from_params(request, db_config)
        sprint_id = request.args.get('id')
        cursor.execute(f'''
            CALL get_sprint_item_composition({sprint_id});
        ''')
        res = get_res(cursor=cursor)
        db.close()
        return {"item_compositions": res}
    except Exception as e:
        db.close()
        return {"error": str(e.__class__.__name__), "message": str(e)}

def update_sprint(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        req = request.get_json()
        organisation_id = get_user_organisation(req, db_config)
        sprint_id = req["sprint"]
        sprint_number = req["sprint_number"]
        start_date = req["start_date"]
        duration = req["duration"]
        definition_of_done = req.get("definition_of_done", None)
        project = req["project"]
        scrum_master = req["scrum_master"]
        cursor.execute(f'''
            UPDATE sprint
            SET sprint_number={sprint_number}, start_date="{start_date}", duration={duration}, definition_of_done="{definition_of_done}", project={project}, scrum_master={scrum_master}
            WHERE id={sprint_id};
        ''')
        db.commit()
        cursor.close()
        db.close()
        return {"message": "Updated!"}
    except Exception as e:
        cursor.close()
        db.close()
        return {"error": str(e.__class__.__name__), "message": str(e)}

def update_sprint_to_complete(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        req = request.get_json()
        organisation_id = get_user_organisation(req, db_config)
        sprint_id = req["sprint"]
        cursor.execute(f'''
            UPDATE sprint
            SET completed={True}
            WHERE id={sprint_id};
        ''')
        db.commit()
        cursor.close()
        db.close()
        return {"message": "Updated!"}
    except Exception as e:
        cursor.close()
        db.close()
        return {"error": str(e.__class__.__name__), "message": str(e)}

def delete_sprint(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        req = request.get_json()
        organisation_id = get_user_organisation(req)
        sprint_id = req["sprint"]
        cursor.execute(f'''
            DELETE FROM sprint
            WHERE id={sprint_id};
        ''')
        db.commit()
        cursor.close()
        db.close()
        return {"message": "Deleted!"}
    except Exception as e:
        cursor.close()
        db.close()
        return {"error": str(e.__class__.__name__), "message": str(e)}