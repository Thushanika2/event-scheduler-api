import re

from flask import jsonify, request

from app.extensions import db
from app.models.organiser_model import Organiser
from app.models.user_model import User


def _validate_organiser_payload(data, organiser_id=None):
    errors = []
    if not data:
        return ["Request body is required."]

    full_name = data.get("full_name")
    if full_name is None or str(full_name).strip() == "":
        errors.append("full_name is required.")

    if organiser_id is None:
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


def create_organiser():
    data = request.get_json(silent=True)
    errors = _validate_organiser_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        user = User(
            email=str(data.get("email")).strip(),
            role="organiser",
            is_active=False,
        )
        user.set_password(str(data.get("password")))
        db.session.add(user)
        db.session.flush()

        organiser = Organiser(
            user_id=user.id,
            full_name=str(data.get("full_name")).strip(),
            organisation=str(data.get("organisation")).strip() if data.get("organisation") else None,
            phone=str(data.get("phone")).strip() if data.get("phone") else None,
        )
        db.session.add(organiser)
        db.session.commit()

        return jsonify({
            "message": "Organiser created successfully.",
            "organiser": organiser.to_dict(),
        }), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_organiser(organiser_id):
    organiser = db.session.get(Organiser, organiser_id)
    if not organiser:
        return jsonify({"error": "Organiser not found."}), 404
    return jsonify({"organiser": organiser.to_dict()}), 200


def update_organiser(organiser_id):
    organiser = db.session.get(Organiser, organiser_id)
    if not organiser:
        return jsonify({"error": "Organiser not found."}), 404

    data = request.get_json(silent=True)
    errors = _validate_organiser_payload(data, organiser_id=organiser_id)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        organiser.full_name = str(data.get("full_name")).strip()
        organiser.organisation = (
            str(data.get("organisation")).strip() if data.get("organisation") else None
        )
        organiser.phone = str(data.get("phone")).strip() if data.get("phone") else None
        db.session.commit()
        return jsonify({
            "message": "Organiser updated successfully.",
            "organiser": organiser.to_dict(),
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def delete_organiser(organiser_id):
    organiser = db.session.get(Organiser, organiser_id)
    if not organiser:
        return jsonify({"error": "Organiser not found."}), 404

    try:
        user = organiser.user
        db.session.delete(organiser)
        if user:
            db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Organiser deleted successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
