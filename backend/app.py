import json
from flask import Flask, request
from flask_cors import CORS

from models.customer import *
from models.employee import *
from models.tester import *
from models.developer import *
from models.project_manager import *
from models.scrum_master import *
from models.project import *
# from models.epic import create_epic, read_epics, update_epic, delete_epic
from models.story import *
from models.item import *
from models.sprint import *
from models.item_type import *
from models.item_status import *

DB_CONFIG = None

app = Flask(__name__)
CORS(app)

#--- Customer ---#
@app.route('/customers', methods = ['POST'])
def post_customers(): 
    return create_customer(request, DB_CONFIG)
@app.route('/customers', methods = ['GET'])
def get_customers(): 
    return read_customers(request, DB_CONFIG)
@app.route('/customers', methods = ['PUT'])
def put_customers(): 
    return update_customer(request, DB_CONFIG)
@app.route('/customers', methods = ['DELETE'])
def delete_customers(): 
    return delete_customer(request, DB_CONFIG)


#--- Employee ---#
@app.route('/employees', methods = ['POST'])
def post_employees():
    return create_employee(request, DB_CONFIG)
@app.route('/employees', methods = ['GET'])
def get_employees():
    return read_employees(request, DB_CONFIG)
@app.route('/employees/full_name', methods = ['GET'])
def get_employee_name():
    return read_employee_name(request, DB_CONFIG)
@app.route('/employees', methods = ['PUT'])
def put_employees():
    return update_employee(request, DB_CONFIG)
@app.route('/employees', methods = ['DELETE'])
def delete_employees():
    return delete_employee(request, DB_CONFIG)


#--- Tester ---#
@app.route('/testers', methods = ['POST'])
def post_testers():
    return create_tester(request, DB_CONFIG)
@app.route('/testers', methods = ['GET'])
def get_testers():
    return read_testers(request, DB_CONFIG)
@app.route('/testers', methods = ['PUT'])
def put_testers():
    return update_tester(request, DB_CONFIG)


#--- Developer ---#
@app.route('/developers', methods = ['POST'])
def post_developers():
    return create_developer(request, DB_CONFIG)
@app.route('/developers', methods = ['GET'])
def get_developers():
    return read_developers(request, DB_CONFIG)
@app.route('/developers', methods = ['PUT'])
def put_developers():
    return update_developer(request, DB_CONFIG)


#--- Scrum master ---#
@app.route('/scrum_masters', methods = ['POST'])
def post_scrummasters():
    return create_scrummaster(request, DB_CONFIG)
@app.route('/scrum_masters', methods = ['GET'])
def get_scrummasters():
    return read_scrummasters(request, DB_CONFIG)


#--- Project manager ---#
@app.route('/project_managers', methods = ['POST'])
def post_projectmanagers():
    return create_projectmanager(request, DB_CONFIG)
@app.route('/project_managers', methods = ['GET'])
def get_projectmanagers():
    return read_projectmanagers(request, DB_CONFIG)


#--- Project ---#
@app.route('/projects', methods = ['POST'])
def post_projects():
    return create_project(request, DB_CONFIG)
@app.route('/projects', methods = ['GET'])
def get_projects():
    return read_projects(request, DB_CONFIG)
@app.route('/projects', methods = ['PUT'])
def put_projects():
    return update_project(request, DB_CONFIG)
@app.route('/projects', methods = ['DELETE'])
def delete_projects():
    return delete_project(request, DB_CONFIG)

"""
#--- Epic ---#
@app.route('/epics', methods = ['POST'])
def post_epics():
    return create_epic(request, DB_CONFIG)
@app.route('/epics', methods = ['GET'])
def get_epics():
    return read_epics(request, DB_CONFIG)
@app.route('/epics', methods = ['PUT'])
def put_epics():
    return update_epic(request, DB_CONFIG)
@app.route('/epics', methods = ['DELETE'])
def delete_epics():
    return delete_epic(request, DB_CONFIG)
"""

#--- Story ---#
@app.route('/stories', methods = ['POST'])
def post_stories():
    return create_story(request, DB_CONFIG)
@app.route('/stories', methods = ['GET'])
def get_stories():
    return read_stories(request, DB_CONFIG)
@app.route('/stories', methods = ['PUT'])
def put_stories():
    return update_story(request, DB_CONFIG)
@app.route('/stories', methods = ['DELETE'])
def delete_stories():
    return delete_story(request, DB_CONFIG)


#--- Item ---#
@app.route('/items', methods = ['POST'])
def post_items():
    return create_item(request, DB_CONFIG)
@app.route('/items', methods = ['GET'])
def get_items():
    return read_items(request, DB_CONFIG)
@app.route('/items/backlog', methods = ['GET'])
def get_backlog_items():
    return read_backlog_items(request, DB_CONFIG)
@app.route('/items', methods = ['PUT'])
def put_items():
    return update_item(request, DB_CONFIG)
@app.route('/items', methods = ['DELETE'])
def delete_items():
    return delete_item(request, DB_CONFIG)


#--- Sprint ---#
@app.route('/sprints', methods = ['POST'])
def post_sprints():
    return create_sprint(request, DB_CONFIG)
@app.route('/sprints', methods = ['GET'])
def get_sprints():
    return read_sprints(request, DB_CONFIG)
@app.route('/sprints/item_composition', methods = ['GET'])
def get_item_composition():
    return read_item_composition(request, DB_CONFIG)
@app.route('/sprints', methods = ['PUT'])
def put_sprints():
    return update_sprint(request, DB_CONFIG)
@app.route('/sprints/complete', methods = ['PUT'])
def put_sprints_complete():
    return update_sprint_to_complete(request, DB_CONFIG)
@app.route('/sprints', methods = ['DELETE'])
def delete_sprints():
    return delete_sprint(request, DB_CONFIG)


#--- Item status ---#
@app.route('/item_statuses', methods = ['GET'])
def get_itemstatuses():
    return read_itemstatuses(request, DB_CONFIG)


#--- Item types ---#
@app.route('/item_types', methods = ['GET'])
def get_itemtypes():
    return read_itemtypes(request, DB_CONFIG)


if __name__ == '__main__':
    CONFIG = None
    with open("./config.json", "rb") as f:
        CONFIG = json.load(f)
    DB_CONFIG = {
        "host": CONFIG["DATABASE"]["HOST"],
        "user": CONFIG["DATABASE"]["USER"],
        "password": CONFIG["DATABASE"]["PASSWORD"],
        "database": CONFIG["DATABASE"]["NAME"]
    }
    app.run(
        host=CONFIG["APPLICATION"]["HOST"],
        port=CONFIG["APPLICATION"]["PORT"], 
        debug=CONFIG["APPLICATION"]["DEBUG"]
    )
