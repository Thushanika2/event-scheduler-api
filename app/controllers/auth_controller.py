import re

from flask import jsonify, request
from flask_jwt_extended import create_access_token, current_user

from app.extensions import db
from app.models.attendee_model import Attendee
from app.models.organiser_model import Organiser
from app.models.user_model import User
from app.utils import PUBLIC_REGISTER_ROLES


def _validate_register_payload(data):
    errors = []
    if not data:
        return ["Request body is required."]

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

    role = str(data.get("role", "attendee")).strip().lower() or "attendee"
    if role == "admin":
        errors.append("Admin accounts can only be created via database seeders.")
    elif role not in PUBLIC_REGISTER_ROLES:
        errors.append("role must be 'attendee' or 'organiser'.")

    full_name = data.get("full_name")
    if full_name is None or str(full_name).strip() == "":
        errors.append("full_name is required.")

    return errors


def _validate_login_payload(data):
    errors = []
    if not data:
        return ["Request body is required."]

    email = data.get("email")
    if email is None or str(email).strip() == "":
        errors.append("email is required.")

    password = data.get("password")
    if password is None or str(password).strip() == "":
        errors.append("password is required.")

    return errors


def register():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_register_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        role = str(data.get("role", "attendee")).strip().lower() or "attendee"
        if role not in PUBLIC_REGISTER_ROLES:
            return jsonify({"error": "Invalid role for registration."}), 400

        user = User(
            email=str(data.get("email")).strip(),
            role=role,
            is_active=False,
        )
        user.set_password(str(data.get("password")))
        db.session.add(user)
        db.session.flush()

        full_name = str(data.get("full_name")).strip()
        phone = str(data.get("phone")).strip() if data.get("phone") else None

        if role == "organiser":
            profile = Organiser(
                user_id=user.id,
                full_name=full_name,
                organisation=str(data.get("organisation")).strip() if data.get("organisation") else None,
                phone=phone,
            )
            db.session.add(profile)
        else:
            profile = Attendee(
                user_id=user.id,
                full_name=full_name,
                phone=phone,
            )
            db.session.add(profile)

        db.session.commit()

        profile_key = "organiser" if role == "organiser" else "attendee"
        return jsonify({
            "message": "User registered successfully. Awaiting admin approval.",
            "user": user.to_dict(),
            profile_key: profile.to_dict(),
        }), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_login_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        email_str = str(data.get("email")).strip()
        user = User.query.filter_by(email=email_str).first()

        if not user or not user.check_password(str(data.get("password"))):
            return jsonify({"error": "Invalid email or password."}), 401

        if not user.is_active:
            return jsonify({"error": "Account is pending admin approval."}), 403

        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "message": "Login successful.",
            "access_token": access_token,
            "user": user.to_dict(),
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def logout():
    return jsonify({"message": "Logout successful."}), 200


def profile():
    user = current_user
    if not user:
        return jsonify({"error": "User not found."}), 404

    payload = {"user": user.to_dict()}
    if user.role == "organiser" and user.organiser:
        payload["organiser"] = user.organiser.to_dict()
    if user.role == "attendee" and user.attendee:
        payload["attendee"] = user.attendee.to_dict()

    return jsonify(payload), 200
