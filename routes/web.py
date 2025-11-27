from flask import Blueprint, render_template
from models.user import get_user
from models.task import get_tasks
from models.concecense import get_concecenses

web_bp = Blueprint("web", __name__)


@web_bp.route('/')
def home(): 
    user = get_user()
    tasks = get_tasks()
    concecenses = get_concecenses()
    return render_template('pages/index.html', tasks = tasks, user=user, concecenses = concecenses)