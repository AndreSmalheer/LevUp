# Solo Leveling Task System

This project is meant to recreate the system from _Solo Leveling_ to help motivate you.

---

## Features

- Add tasks
- Edit tasks
- Remove tasks
- Set recurring tasks (for example, every Monday)
- Set a start time for a task (e.g., 12:00). The task won’t be visible until then.
- Set an end time for a task. If you do not complete the task by the end time, you fail the task and must do a punishment.

> By default, tasks automatically fail at 00:01, so if you don’t complete a task by the end of the day, you need to perform a punishment. You can earn coins and XP by completing tasks. If you gain enough XP, you level up.

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/AndreSmalheer/LevUp
   cd LevUp
   ```

2. - Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. run Aplication
   python app.py
   ```bash
   python app.py
   ```

## Tools Used

- Flask for hosting the server
- Python for backend interaction and database management
- Database for data storage
- JavaScript for logic
- HTML/CSS for styling
