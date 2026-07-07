import re

from flask import jsonify, request
from flask_jwt_extended import current_user

from app.extensions import db
from app.models.attendee_model import Attendee
from app.models.user_model import User


def _validate_attendee_payload(data, attendee_id=None):
    errors = []
    if not data:
        return ["Request body is required."]

    full_name = data.get("full_name")
    if full_name is None or str(full_name).strip() == "":
        errors.append("full_name is required.")

    if attendee_id is None:
        email = data.get("email")
        if email is None or str(email).strip() == "":
            errors.append("email is required.")
        else:
            email_str = str(email).strip()
            email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(email_regex, email_str):
                errors.append("Invalid email format.")
            elif User.query.filter_by(email=email_str).first():
                errors.append("Email address already exists.")

        password = data.get("password")
        if password is None or str(password).strip() == "":
            errors.append("password is required.")
        elif len(str(password)) < 6:
            errors.append("password must be at least 6 characters long.")

    return errors


def create_attendee():
    data = request.get_json(silent=True)
    errors = _validate_attendee_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        user = User(
            email=str(data.get("email")).strip(),
            role="attendee",
            is_active=False,
        )
        user.set_password(str(data.get("password")))
        db.session.add(user)
        db.session.flush()

        attendee = Attendee(
            user_id=user.id,
            full_name=str(data.get("full_name")).strip(),
            phone=str(data.get("phone")).strip() if data.get("phone") else None,
        )
        db.session.add(attendee)
        db.session.commit()

        return jsonify({
            "message": "Attendee created successfully.",
            "attendee": attendee.to_dict(),
        }), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_attendee(attendee_id):
    attendee = db.session.get(Attendee, attendee_id)
    if not attendee:
        return jsonify({"error": "Attendee not found."}), 404
    return jsonify({"attendee": attendee.to_dict()}), 200


def update_attendee(attendee_id):
    attendee = db.session.get(Attendee, attendee_id)
    if not attendee:
        return jsonify({"error": "Attendee not found."}), 404

    data = request.get_json(silent=True)
    errors = _validate_attendee_payload(data, attendee_id=attendee_id)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        attendee.full_name = str(data.get("full_name")).strip()
        attendee.phone = str(data.get("phone")).strip() if data.get("phone") else None
        db.session.commit()
        return jsonify({
            "message": "Attendee updated successfully.",
            "attendee": attendee.to_dict(),
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def delete_attendee(attendee_id):
    attendee = db.session.get(Attendee, attendee_id)
    if not attendee:
        return jsonify({"error": "Attendee not found."}), 404

    try:
        user = attendee.user
        db.session.delete(attendee)
        if user:
            db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Attendee deleted successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
