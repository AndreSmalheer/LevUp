from models.task import get_tasks
from models.user import get_user

def reset_task():
    from datetime import datetime, timedelta
    import requests 

    tasks = get_tasks()   
    user = get_user()

    API_URL = "http://localhost:5000/api/update"

    today = datetime.today().strftime("%A").lower()
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%A").lower()

    payload_carachter_stats = {
            "type": "update_user_stats",
            "user_id": user['id'],
            "level": user['level'],
            "coins": user['coins'],
            "xp": user['xp'],
            "xp_to_next_level": user['xp_to_next_level'],
            "last_task_reset": datetime.today().strftime("%Y-%m-%d"),
    }

    requests.post(API_URL, json=payload_carachter_stats)

    for task in tasks:
        task_id = task['task_id']
        failed = task['failed']
        hidden = task['hidden']
        completed = task['completed']
        reward_coins = task['coin_reward']
        reward_xp = task['xp_reward']
        start_time = task['start_time']
        end_time = task['end_time']
        penelty_id = task['penelty_id']

        repeat_days = task['repeat_days']
        if not isinstance(repeat_days, list):
         repeat_days_list = [repeat_days] if repeat_days else []


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
                    payload["hidden"] = False
                    requests.post(API_URL, json=payload)
                    continue
                else:
                    # Hide and reset
                    payload["hidden"] = True
                    payload["completed"] = False
                    payload["failed"] = False
                    requests.post(API_URL, json=payload)
                    continue
            else:
                # remove the task
                requests.post("http://localhost:5000/api/remvoe", json={
                "type": "remove_task",
                "task_id": task_id
                })
                continue

        # ---------------------------
        # 3. TASKS THAT SHOULD RUN TODAY OR WERE MISSED YESTERDAY
        # ---------------------------
        if repeat_days:
            if not bool(hidden):
                if today in repeat_days:
                    if yesterday in repeat_days:
                        payload["failed"] = True
                        payload["completed"] = False
                        payload["hidden"] = False
                        requests.post(API_URL, json=payload)
            
                        requests.post("http://localhost:5000/api/add", json={
                            "type": "add_task",
                            "task_name": task['task_name'],
                            "coin_reward": reward_coins,
                            "xp_reward": reward_xp,
                            "start_time": start_time,
                            "end_time": end_time,
                            "repeat_days": repeat_days_list
                        })
                        continue
                    else:
                        requests.post(API_URL, json=payload)
                    continue
            
                elif yesterday in repeat_days:
                    payload["failed"] = True
                    payload["completed"] = False
                    payload["hidden"] = False
                    requests.post(API_URL, json=payload)
                    continue

            else:
                if today in repeat_days:
                 payload["failed"] = False
                 payload["completed"] = False
                 payload["hidden"] = False
                 requests.post(API_URL, json=payload)
                 continue  

                continue 
    

        # ---------------------------
        # 4. PENDING TASKS NOT SCHEDULED TODAY
        # ---------------------------
        payload["failed"] = True
        payload["completed"] = False
        payload["hidden"] = False
        requests.post(API_URL, json=payload)