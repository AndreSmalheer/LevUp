from flask import Flask, render_template
from database.user_queries import get_user
from database.task_queries import get_tasks, mark_task_failed, delete_task_from_db
from helpers.task_helpers import insert_task
from routes.tasks import delete_task
from routes.tasks import tasks_bp
from routes.user import user_bp
from flask_apscheduler import APScheduler
from datetime import datetime
from database.db import get_connection

app = Flask(__name__)
scheduler = APScheduler()

def reset_tasks():
    tasks = get_tasks()
    new_tasks = [] 

    for task in tasks:
        repeat_days = task['repeat_days']
        completed = task['completed']
        failed = task['failed']

        if repeat_days:
            if not completed and not failed:
                mark_task_failed(task['task_id'])

                conn = get_connection()
                user = get_user()
                task_name = task['task_name']
                coin_reward = task['coin_reward']
                xp_reward = task['xp_reward']
                start_time = task['start_time']
                end_time = task['end_time']
                repeat_days_list = repeat_days.split(",") if repeat_days else []
                repeat_days_str = ",".join(repeat_days_list) if repeat_days_list else None

                new_task_id = insert_task(conn, user["id"], task_name, coin_reward, xp_reward, start_time, end_time, repeat_days_str)

                for t in get_tasks():
                    if t['task_id'] == new_task_id:
                        new_tasks.append(t)
                        break

        else:
            if completed:
                delete_task_from_db(task['task_id'])
            elif not failed:
                mark_task_failed(task['task_id'])

    tasks.extend(new_tasks)
 
# def daily_task():
#     print(f"Task running at {datetime.now()}")


# scheduler.add_job(
#     id='daily_task',
#     func=daily_task,
#     trigger='cron',
#     hour=7,
#     minute=1
# )

# scheduler.init_app(app)
# scheduler.start()

# Register blueprints
app.register_blueprint(tasks_bp)
app.register_blueprint(user_bp)

@app.route('/')
def home():
    user = get_user()
    tasks = get_tasks()
    return render_template('index.html', user=user, tasks=tasks)

if __name__ == '__main__':
    reset_tasks()
    app.run(host="0.0.0.0", port=5000, debug=True)

    
