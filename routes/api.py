from flask import Blueprint, request, jsonify
from models.db import get_connection
from models.user import get_user
from scheduler.tasks import reset_task

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/add", methods=["POST"])
def add_item():
    data = request.get_json(silent=True) or request.form
    data_type = data.get("type")

    print(f"Adding new item of type: {data_type}")

    conn = get_connection()
    cursor = conn.cursor()

    if data_type == "add_user":
        name = request.form.get("user_name")
    
        # Insert user
        cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
        user_id = cursor.lastrowid
    
        # Insert default stats
        cursor.execute(
            "INSERT INTO character_stats (user_id, level, coins, xp, xp_to_next_level) VALUES (?, ?, ?, ?, ?)",
            (user_id, 1, 0, 0, 100)
        )
    
        conn.commit()
        cursor.close()
        conn.close()
    
        return {
            "status": "success",
            "data": {
                "id": user_id,
                "name": name,
                "level": 1,
                "coins": 0,
                "xp": 0,
                "xp_to_next_level": 100
            }
        }
    
    if data_type == "add_task":
       data = request.get_json(silent=True) or request.form

       user = get_user()
       user_id = user["id"]

       task_name = data.get("task_name")
       coin_reward = data.get("coin_reward")
       xp_reward = data.get("xp_reward")
       start_time = data.get("start_time") or None
       end_time = data.get("end_time") or None

       # Handle repeat_days properly for both JSON and form
       if isinstance(data.get("repeat_days"), list):
           repeat_days = data.get("repeat_days")
       else:
           repeat_days = request.form.getlist("repeat_days") or []
       repeat_days_str = ",".join(repeat_days) if repeat_days else None

       cursor.execute('''
           INSERT INTO tasks (user_id, task_name, coin_reward, xp_reward, start_time, end_time, repeat_days)
           VALUES (?, ?, ?, ?, ?, ?, ?)
       ''', (user_id, task_name, coin_reward, xp_reward, start_time, end_time, repeat_days_str))
       task_id = cursor.lastrowid
       conn.commit()
       cursor.close()

       task_dict = {
           "task_id": task_id,
           "task_name": task_name,
           "coin_reward": coin_reward,
           "xp_reward": xp_reward,
           "start_time": start_time,
           "end_time": end_time,
           "repeat_days": repeat_days
       }

       return jsonify({"status": "success", "message": "Task added!", "task": task_dict})

    if data_type == "add_concecense":
       data = request.get_json(silent=True) or request.form

       concecenses_name = data.get("concecenses_name")
       concecenses_description = data.get("concecenses_description")

       cursor = conn.cursor()
       cursor.execute('''
           INSERT INTO concecenses (name, description)
           VALUES (?, ?)
       ''', (concecenses_name, concecenses_description))
       
       concecenses_id = cursor.lastrowid 
       conn.commit()
       cursor.close()

       concecenses_dict = {
         "concecenses_id": concecenses_id,
         "name": concecenses_name,
         "description": concecenses_description
       }

       return jsonify({"status": "success", "message": "concecenses added!", "concecenses": concecenses_dict})

    return jsonify({"status": "Failed", "message": "Data type does not match"})

@api_bp.route("/api/remvoe", methods=["POST"])
def remove_item():
    data_type = request.json.get("type") 

    if data_type == "remove_task":
        task_id = request.json.get("task_id")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))

        conn.commit()
        conn.close()

        return jsonify({"message": "Task removed"}), 200
    
    if data_type == "remove_consequence":
        consequence_id = request.json.get("consequence_id")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM concecenses WHERE concecenses_id = ?', (consequence_id,))

        conn.commit()
        conn.close()

        return jsonify({"message": "Task removed"}), 200

    return jsonify({"status": "Failed", "message": "Data type does not match"})

@api_bp.route("/api/update", methods=["POST"])
def update_item():
    data_type = request.json.get("type") 

    if data_type == "update_task":
        task_id = request.json.get("task_id")
        name = request.json.get("task_name")
        coin_reward = request.json.get("coin_reward")
        xp_reward = request.json.get("xp_reward")
        start_time = request.json.get("start_time")
        end_time = request.json.get("end_time")
        completed = request.json.get("completed")
        failed = request.json.get("failed")
        repeat_days = request.json.get("repeat_days")
        penelty_id = request.json.get("penelty_id")
        repeat_days_list = [repeat_days] if isinstance(repeat_days, str) else repeat_days
        repeat_days_string = ",".join(repeat_days_list) if repeat_days_list else None

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('''
        UPDATE tasks
        SET task_name = ?, coin_reward = ?, xp_reward = ?, start_time = ?, end_time = ?,
            completed = ?, failed = ?, penelty_id = ?, repeat_days = ?
        WHERE id = ?
        ''', (name, coin_reward, xp_reward, start_time, end_time, completed, failed, penelty_id,  repeat_days_string, task_id))

        conn.commit()
        conn.close()

        return jsonify({"message": "Task updated"}), 200

    if data_type == "update_concecenses":
        id = request.json.get("id")
        name = request.json.get("name")
        description = request.json.get("description")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('''
        UPDATE concecenses
        SET name = ?, description = ?
        WHERE concecenses_id = ?
        ''', (name, description, id))

        conn.commit()
        conn.close()

        return jsonify({"message": "concecense updated"}), 200

    if data_type == "update_user_stats":
        user_id = request.json.get("user_id")
        level = request.json.get("level")
        coins = request.json.get("coins")
        xp = request.json.get("xp")
        xp_to_next_level = request.json.get("xp_to_next_level")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('''
        UPDATE character_stats
        SET level = ?, coins = ?, xp = ?, xp_to_next_level = ?
        WHERE user_id = ?
        ''', (level, coins, xp, xp_to_next_level, user_id))

        conn.commit()
        conn.close()

        return jsonify({"message": "User stats updated"}), 200
    
    if data_type == "update_user_settings":
        new_user_name = request.json.get("user_name")
        user_id = request.json.get("user_id")

        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users
            SET name = ?
            WHERE id = ?
        ''', (new_user_name, user_id))

        conn.commit()
        conn.close()

        return jsonify({"message": "user settings updated"}), 200

    return jsonify({"status": "Failed", "message": "Data type does not match"})

@api_bp.route("/api/resetAllTasks",  methods=["POST"])
def resetAllTasks():
    reset_task()
    return "Tasks reset", 200