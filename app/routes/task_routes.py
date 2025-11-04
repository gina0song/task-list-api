from flask import Blueprint, request, jsonify, make_response
from ..models.task import Task
from ..db import db
from .route_utilities import validate_model, create_model
from datetime import datetime
import os
import requests


SLACK_API_URL = "https://slack.com/api/chat.postMessage"
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks') 

# Route Helper Method
def validate_task(id):
    return validate_model(Task, id)


# CRUD Routes
@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    task_dict, status_code = create_model(Task, request_body)
    return jsonify(task_dict), status_code

@tasks_bp.get("")
def get_tasks():
    sort_by = request.args.get('sort')
    
    # Sort tasks if sort parameter is provided,"asc" for ascending and "desc" for descending
    if sort_by == 'asc':
        query = db.select(Task).order_by(Task.title.asc())
    elif sort_by == 'desc':
        query = db.select(Task).order_by(Task.title.desc())
    else:
        query = db.select(Task)
    
    tasks = db.session.scalars(query).all()

    return jsonify([task.to_dict() for task in tasks]), 200

@tasks_bp.get("/<id>")
def get_single_task(id):
    task = validate_task(id)

    return jsonify(task.to_dict()), 200

# Mark Task as Complete
@tasks_bp.patch("/<id>/mark_complete")
def mark_complete(id):
    task = validate_task(id) 
    task.completed_at = datetime.now()
    
    db.session.commit()

    # Send Slack notification
    if SLACK_BOT_TOKEN:
            message = f"Someone just completed the task {task.title}"
            
            headers = {
                'Content-type': 'application/json',
                'Authorization': f'Bearer {SLACK_BOT_TOKEN}'
            }
            
            notification_data = {
                "channel": "task-notifications", 
                "text": message
            }
            response = requests.post(SLACK_API_URL, json=notification_data, headers=headers)

            if response.status_code != 200:
                print(f"Error sending Slack notification: {response.text}")

    return jsonify(task.to_dict()), 204

# Mark Task as Incomplete
@tasks_bp.patch("/<id>/mark_incomplete")
def mark_incomplete(id):
    task = validate_task(id)

    task.completed_at = None

    db.session.commit()

    return make_response(jsonify({}), 204)


@tasks_bp.put("/<id>")
def update_task(id):
    task = validate_task(id)

    request_body = request.get_json()

    if "title" in request_body:
        task.title = request_body["title"]
    
    if "description" in request_body:
        task.description = request_body["description"]

    db.session.commit()

    return "", 204

@tasks_bp.delete("/<id>")
def delete_task(id):
    task = validate_task(id)

    db.session.delete(task)
    db.session.commit()

    return "", 204


