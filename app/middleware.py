from functools import wraps

from flask import jsonify
from flask_jwt_extended import current_user, verify_jwt_in_request


def jwt_required_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        if not current_user:
            return jsonify({"error": "User not found."}), 404
        return fn(*args, **kwargs)

    return wrapper


def roles_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            if not current_user:
                return jsonify({"error": "User not found."}), 404
            if current_user.role not in roles:
                return jsonify({"error": "Access forbidden: insufficient permissions."}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def attendee_owner_required(fn):
    @wraps(fn)
    def wrapper(attendee_id, *args, **kwargs):
        verify_jwt_in_request()
        if not current_user:
            return jsonify({"error": "User not found."}), 404
        if current_user.role != "attendee":
            return jsonify({"error": "Access forbidden: insufficient permissions."}), 403
        if not current_user.attendee or current_user.attendee.id != attendee_id:
            return jsonify({"error": "Access forbidden: insufficient permissions."}), 403
        return fn(attendee_id, *args, **kwargs)

    return wrapper


def organiser_owner_required(fn):
    @wraps(fn)
    def wrapper(organiser_id, *args, **kwargs):
        verify_jwt_in_request()
        if not current_user:
            return jsonify({"error": "User not found."}), 404
        if current_user.role != "organiser":
            return jsonify({"error": "Access forbidden: insufficient permissions."}), 403
        if not current_user.organiser or current_user.organiser.id != organiser_id:
            return jsonify({"error": "Access forbidden: insufficient permissions."}), 403
        return fn(organiser_id, *args, **kwargs)

    return wrapper
