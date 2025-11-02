from flask import Blueprint, make_response, request,abort, jsonify
from ..models.task import Task
from ..db import db
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks') 

# Route Helper Method
def validate_task(ID):
    try:
        ID = int(ID)
    except ValueError:
        invalid = {"message": f"Task ID ({ID}) is invalid."}
        abort(make_response(invalid, 400))

    query = db.select(Task).where(Task.id == ID)
    task = db.session.scalar(query)
    if not task:
        not_found = {"message": f"Task with ID ({ID}) not found."}
        abort(make_response(not_found, 404))

    return task


# CRUD Routes
@tasks_bp.post("")
def create_task():
    # (try and except block) necessary to catch the KeyError when title or description is missing. 
    try:
        request_body = request.get_json()

        new_task = Task.from_dict(request_body)

        db.session.add(new_task)
        db.session.commit()

        task_response = new_task.to_dict()

        return jsonify(task_response), 201
    
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"message": "Internal Server Error"}), 500

@tasks_bp.get("")
def get_tasks():
    sort_by = request.args.get('sort')
    query = db.select(Task)
    all_tasks = db.session.scalars(query).all()

    # Sort tasks if sort parameter is provided,"asc" for ascending and "desc" for descending
    if sort_by == 'asc':
        all_tasks.sort(key=lambda task: task.title, reverse=False)
    elif sort_by == 'desc':
        all_tasks.sort(key=lambda task: task.title, reverse=True)

    tasks_response = [task.to_dict() for task in all_tasks]

    return jsonify(tasks_response), 200


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
    
    return make_response(jsonify({}), 204)

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


