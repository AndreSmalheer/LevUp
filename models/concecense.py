from models.db import get_connection

def get_concecenses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM concecenses")
    rows = cursor.fetchall()
    concecenses = [{
        "concecenses_id": row["concecenses_id"],
        "name": row["name"],
        "description": row["description"],
    } for row in rows]
    cursor.close()
    conn.close()
    return concecenses
