from flask import Blueprint, make_response, request,abort, jsonify

from app.routes.task_routes import validate_task
from ..models.goal import Goal
from ..db import db
from datetime import datetime
import os
import requests

SLACK_API_URL = "https://slack.com/api/chat.postMessage"
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")     

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')

# Route Helper Method
def validate_goal(ID):
    try:
        ID = int(ID)
    except ValueError:
        invalid = {"message": f"Goal ID ({ID}) is invalid."}
        abort(make_response(invalid, 400))

    query = db.select(Goal).where(Goal.id == ID)
    goal = db.session.scalar(query)
    if not goal:
        not_found = {"message": f"Goal with ID ({ID}) not found."}
        abort(make_response(not_found, 404))

    return goal

# CRUD Routes
@goals_bp.post("")
def create_goal():
    try:
        request_body = request.get_json()

        new_goal = Goal.from_dict(request_body)

        db.session.add(new_goal)
        db.session.commit()

        goal_response = new_goal.to_dict()

        return jsonify(goal_response), 201
    
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    
@goals_bp.get("")
def get_goals():
    goals = db.session.scalars(db.select(Goal)).all()
    return jsonify([goal.to_dict() for goal in goals]), 200     

@goals_bp.get("/<id>")  
def get_goal(id):
    goal = validate_goal(id)
    return jsonify(goal.to_dict()), 200 

@goals_bp.put("/<id>")
def update_goal(id):
    goal = validate_goal(id)

    request_body = request.get_json()

    if "title" in request_body:
        goal.title = request_body["title"]

    db.session.commit()

    return "", 204


@goals_bp.delete("/<id>")
def delete_goal(id):
    goal = validate_goal(id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal.id} "{goal.title}" successfully deleted'}), 204


