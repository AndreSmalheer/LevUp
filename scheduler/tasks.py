from models.task import get_tasks

def reset_task():
    from datetime import datetime, timedelta
    import requests 

    tasks = get_tasks()
    API_URL = "http://localhost:5000/api/update"

    today = datetime.today().strftime("%A")
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%A")

    for task in tasks:
        task_id = task['task_id']
        failed = task['failed']
        completed = task['completed']
        repeat_days = task['repeat_days']
        reward_coins = task['coin_reward']
        reward_xp = task['xp_reward']
        start_time = task['start_time']
        end_time = task['end_time']
        penelty_id = task['penelty_id']

        repeat_days_string = ",".join(repeat_days) if repeat_days else None

        # Data template for update_task
        payload = {
            "type": "update_task",
            "task_id": task_id,
            "task_name": task['task_name'],
            "coin_reward": reward_coins,
            "xp_reward": reward_xp,
            "start_time": start_time,
            "end_time": end_time,
            "repeat_days": repeat_days,
            "penelty_id": penelty_id,
            "completed": completed,
            "failed": failed
        }

        # ---------------------------
        # 1. FAILED TASKS
        # ---------------------------
        if failed:
            if today in repeat_days:
                # Skip → Do nothing
                continue
            else:
                # Skip task that does not repeat today
                continue

        # ---------------------------
        # 2. COMPLETED TASKS
        # ---------------------------
        if completed:
            if repeat_days:
                if today in repeat_days:
                    # Reset completed and failed = FALSE
                    payload["completed"] = False
                    payload["failed"] = False
                    requests.post(API_URL, json=payload)
                    continue
                else:
                    # Hide and reset
                    payload["completed"] = False
                    payload["failed"] = False
                    requests.post(API_URL, json=payload)
                    continue
            else:
                # Remove/ignore → no update needed
                continue

        # ---------------------------
        # 3. TASKS THAT SHOULD RUN TODAY OR WERE MISSED YESTERDAY
        # ---------------------------
        if repeat_days: 
            if today in repeat_days:
                if yesterday in repeat_days:
                    # Mark as failed because yesterday was missed
                    payload["failed"] = True
                    payload["completed"] = False
                    requests.post(API_URL, json=payload)
                else:
                    # Normal scheduling (no status change)
                    requests.post(API_URL, json=payload)
                continue

            elif yesterday in repeat_days:
                # Was scheduled yesterday but NOT today → mark failed, no new task
                payload["failed"] = True
                payload["completed"] = False
                requests.post(API_URL, json=payload)
                continue

        # ---------------------------
        # 4. PENDING TASKS NOT SCHEDULED TODAY
        # ---------------------------
        payload["failed"] = True
        payload["completed"] = False
        requests.post(API_URL, json=payload)