import sqlite3
from database.db import get_connection

def insert_consequence(consequence_name, consequence_description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO consequences (consequence_name, consequence_description)
        VALUES (?, ?)
    ''', (consequence_name, consequence_description))
    consequence_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return consequence_id
