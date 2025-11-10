from flask import Blueprint, jsonify, request
import sqlite3
from helpers.consequence_helpers import insert_consequence

consequence_bp = Blueprint('tasks', __name__)

@consequence_bp.route('/add_consequence', methods=['POST'])
def add_consequence():

    consequence_name = request.form.get('consequence_name')
    consequence_description = request.form.get('consequence_description')

    consequence_id = insert_consequence(consequence_name ,consequence_description)

    task_dict = {
        "consequence_id": consequence_id,
        "consequence_name": consequence_name,
        "consequence_description": consequence_description
    }
    
    return jsonify({"status": "success", "message": "consequence added!", "task": task_dict})