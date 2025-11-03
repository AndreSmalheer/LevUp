from flask import Blueprint
from database.user_queries import add_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/user_info')
def user_info():
    return "User info here"


@user_bp.route('/create_user/<name>')
def create_user(name):
    data = add_user(name)
    return data