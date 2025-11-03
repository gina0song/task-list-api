import os
from flask import Blueprint, make_response, request, jsonify

from app import db
from ..models.goal import Goal
from .route_utilities import validate_model, create_model, get_all_models, update_model, delete_model
from .task_routes import validate_task

SLACK_API_URL = "https://slack.com/api/chat.postMessage"
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")     

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')

# Route Helper Method
def validate_goal(id):
    return validate_model(Goal,id)

# CRUD Routes
@goals_bp.post("")
def create_goal():
    request_body = request.get_json()
    goal_dict, status_code = create_model(Goal, request_body)
    return jsonify(goal_dict), status_code

@goals_bp.get("")
def get_goals():
    goals_list, status_code = get_all_models(Goal)
    return jsonify(goals_list), status_code


@goals_bp.get("/<id>")  
def get_goal(id):
    goal = validate_goal(id)
    return jsonify(goal.to_dict()), 200 

@goals_bp.put("/<id>")
def update_goal(id):
    goal = validate_goal(id)
    request_body = request.get_json()
    update_model(goal, request_body, ['title'])
    return "", 204


@goals_bp.delete("/<id>")
def delete_goal(id):
    goal = validate_goal(id)
    response_dict, status_code = delete_model(goal)
    return jsonify(response_dict), status_code



@goals_bp.post("/<id>/tasks")
def post_tasks_to_goal(id):
    goal = validate_goal(id)
    
    request_body = request.get_json()
    task_ids = request_body.get("task_ids", [])
    
    goal.tasks = []
    
    for task_id in task_ids:
        task = validate_task(task_id)  
        goal.tasks.append(task)
    
    db.session.commit()
    
    return jsonify({"id": goal.id, "task_ids": task_ids}), 200

@goals_bp.get("/<id>/tasks")
def get_tasks_for_goal(id):

    goal = validate_goal(id)

    response_body = goal.to_dict()
    response_body.pop('task_ids', None) 

    task_dicts = [task.to_dict() for task in goal.tasks]
    
    response_body["tasks"] = task_dicts

    return make_response(response_body, 200)