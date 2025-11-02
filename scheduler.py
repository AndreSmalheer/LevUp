from flask_apscheduler import APScheduler
from database.task_queries import get_tasks, mark_task_failed, delete_task_from_db
from database.user_queries import get_user
from database.db import get_connection
from helpers.task_helpers import insert_task

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
                new_task_id = insert_task(
                    conn,
                    user["id"],
                    task["task_name"],
                    task["coin_reward"],
                    task["xp_reward"],
                    task["start_time"],
                    task["end_time"],
                    task["repeat_days"]
                )

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

def init_scheduler(app):
    scheduler.init_app(app)
    scheduler.add_job(
        id='daily task reset',
        func=reset_tasks,
        trigger='cron',
        hour=0,
        minute=1
    )
    scheduler.start()