from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from routes.api import api_bp
from routes.web import web_bp
from scheduler.tasks import reset_task

app = Flask(__name__)
app.register_blueprint(api_bp)
app.register_blueprint(web_bp)


if __name__ == '__main__':  
    scheduler = BackgroundScheduler()
    scheduler.add_job(reset_task, 'cron', hour=0, minute=1)
    scheduler.start()

    app.run(host="0.0.0.0", port=5000, debug=True)
