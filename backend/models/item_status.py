import mysql.connector
from util.utils import get_res

def read_itemstatuses(request, db_config):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        cursor.execute(f'''
            SELECT *
            FROM item_status;
        ''')
        res = get_res(cursor=cursor)
        db.close()
        return {"item_statuses": res}
    except Exception as e:
        db.close()
        return {"error": str(e.__class__.__name__), "message": str(e)}