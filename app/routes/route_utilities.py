from flask import abort, make_response, jsonify
from ..db import db


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        error_message = {
            "message": f"{cls.__name__} ID ({model_id}) is invalid."
        }
        abort(make_response(jsonify(error_message), 400))
    
    query = db.select(cls).where(cls.id == model_id)
    instance = db.session.scalar(query)
    
    if not instance:
        error_message = {
            "message": f"{cls.__name__} with ID ({model_id}) not found."
        }
        abort(make_response(jsonify(error_message), 404))
    
    return instance


def create_model(cls, request_body):
    try:
        new_instance = cls.from_dict(request_body)
        db.session.add(new_instance)
        db.session.commit()
        
        return new_instance.to_dict(), 201
        
    except KeyError:
        error_message = {"details": "Invalid data"}
        abort(make_response(jsonify(error_message), 400))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        error_message = {"message": "Internal Server Error"}
        abort(make_response(jsonify(error_message), 500))


def get_all_models(cls):
    instances = db.session.scalars(db.select(cls)).all()
    return [instance.to_dict() for instance in instances], 200


def update_model(instance, request_body, fields_to_update):
    for field in fields_to_update:
        if field in request_body:
            setattr(instance, field, request_body[field])
    
    db.session.commit()
    return "", 204


def delete_model(instance):
    model_name = instance.__class__.__name__
    model_id = instance.id
    title = getattr(instance, 'title', 'N/A')
    
    db.session.delete(instance)
    db.session.commit()
    
    response = {
        "details": f'{model_name} {model_id} "{title}" successfully deleted'
    }
    return response, 204
