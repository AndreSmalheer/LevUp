import sqlite3
from database.db import get_connection

# ----------------- Character Stats -----------------
def get_character_stats(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM character_stats LIMIT 1")
    stats = cursor.fetchone()
    cursor.close()
    return stats

def update_character_stats(conn, level, coins, xp, xp_to_next_level):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE character_stats
        SET level = ?, coins = ?, xp = ?, xp_to_next_level = ?
    """, (level, coins, xp, xp_to_next_level))
    conn.commit()
    cursor.close()

# ----------------- Task Helpers -----------------
def get_task_by_name(conn, task_name):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE task_name = ?", (task_name,))
    task = cursor.fetchone()
    cursor.close()
    return task

def mark_task_completed(conn, task_name, completed=True):
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = ? WHERE task_name = ?", (completed, task_name))
    conn.commit()
    cursor.close()

def insert_task(conn, user_id, task_name, coin_reward, xp_reward, start_time=None, end_time=None, repeat_days=None):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO tasks (user_id, task_name, coin_reward, xp_reward, start_time, end_time, repeat_days)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, task_name, coin_reward, xp_reward, start_time, end_time, repeat_days))
    task_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    return task_id

def update_task_in_db(conn, user_id, task_id, task_name, coin_reward, xp_reward, start_time, end_time, repeat_days):
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE tasks
    SET task_name = ?, coin_reward = ?, xp_reward = ?, start_time = ?, end_time = ?, repeat_days = ?
    WHERE user_id = ? AND id = ?
    ''', (task_name, coin_reward, xp_reward, start_time, end_time, repeat_days, user_id, task_id))
    conn.commit()
    cursor.close()

# ----------------- XP and Level Calculations -----------------
def calculate_xp_and_level_up(current_xp, xp_reward, level, xp_to_next_level):
    new_xp = current_xp + xp_reward
    new_level = level
    new_xp_to_next_level = xp_to_next_level

    while new_xp >= new_xp_to_next_level:
        new_xp -= new_xp_to_next_level
        new_level += 1
        new_xp_to_next_level = int(new_xp_to_next_level * 1.2)

    return new_xp, new_level, new_xp_to_next_level

def calculate_xp_and_level_down(current_xp, xp_reward, level, xp_to_next_level):
    new_xp = current_xp - xp_reward
    new_level = level
    new_xp_to_next_level = xp_to_next_level

    while new_xp < 0 and new_level > 1:
        new_level -= 1
        new_xp_to_next_level = int(new_xp_to_next_level / 1.2)
        new_xp += new_xp_to_next_level

    if new_level == 1 and new_xp < 0:
        new_xp = 0

    return new_xp, new_level, new_xp_to_next_level
