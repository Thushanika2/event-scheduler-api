from flask import jsonify, request
from flask_jwt_extended import current_user

from app.extensions import db
from app.models.agenda_model import AgendaItem
from app.models.session_model import Session
from app.utils import parse_datetime


def _validate_session_payload(data):
    errors = []
    if not data:
        return ["Request body is required."]

    for field in ("title", "speaker", "track", "room", "start_time", "end_time", "capacity"):
        value = data.get(field)
        if value is None or (isinstance(value, str) and value.strip() == ""):
            errors.append(f"{field} is required.")

    if not errors:
        try:
            start = parse_datetime(data.get("start_time"))
            end = parse_datetime(data.get("end_time"))
            if start >= end:
                errors.append("end_time must be after start_time.")
        except (TypeError, ValueError):
            errors.append("start_time and end_time must be valid ISO datetime strings.")

        try:
            capacity = int(data.get("capacity"))
            if capacity < 1:
                errors.append("capacity must be at least 1.")
        except (TypeError, ValueError):
            errors.append("capacity must be a valid integer.")

    return errors


def _session_enrollment_count(session_id):
    return AgendaItem.query.filter_by(session_id=session_id).count()


def _session_to_public_dict(session):
    data = session.to_dict()
    enrolled = _session_enrollment_count(session.id)
    data["enrolled_count"] = enrolled
    data["is_full"] = enrolled >= session.capacity
    return data


def create_session():
    data = request.get_json(silent=True)
    errors = _validate_session_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    if not current_user.organiser:
        return jsonify({"error": "Organiser profile not found."}), 404

    try:
        session = Session(
            organiser_id=current_user.organiser.id,
            title=str(data.get("title")).strip(),
            speaker=str(data.get("speaker")).strip(),
            track=str(data.get("track")).strip(),
            room=str(data.get("room")).strip(),
            start_time=parse_datetime(data.get("start_time")),
            end_time=parse_datetime(data.get("end_time")),
            capacity=int(data.get("capacity")),
        )
        db.session.add(session)
        db.session.commit()
        return jsonify({
            "message": "Session created successfully.",
            "session": _session_to_public_dict(session),
        }), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_sessions():
    query = Session.query

    track = request.args.get("track")
    if track:
        query = query.filter(Session.track == track.strip())

    start_after = request.args.get("start_after")
    if start_after:
        try:
            query = query.filter(Session.start_time >= parse_datetime(start_after))
        except (TypeError, ValueError):
            return jsonify({"error": "start_after must be a valid ISO datetime string."}), 400

    start_before = request.args.get("start_before")
    if start_before:
        try:
            query = query.filter(Session.start_time <= parse_datetime(start_before))
        except (TypeError, ValueError):
            return jsonify({"error": "start_before must be a valid ISO datetime string."}), 400

    sessions = query.order_by(Session.start_time.asc()).all()
    return jsonify({"sessions": [_session_to_public_dict(s) for s in sessions]}), 200


def get_session(session_id):
    session = db.session.get(Session, session_id)
    if not session:
        return jsonify({"error": "Session not found."}), 404
    return jsonify({"session": _session_to_public_dict(session)}), 200


def get_organiser_sessions():
    if not current_user.organiser:
        return jsonify({"error": "Organiser profile not found."}), 404

    sessions = (
        Session.query.filter_by(organiser_id=current_user.organiser.id)
        .order_by(Session.start_time.asc())
        .all()
    )
    return jsonify({"sessions": [_session_to_public_dict(s) for s in sessions]}), 200


def update_session(session_id):
    session = db.session.get(Session, session_id)
    if not session:
        return jsonify({"error": "Session not found."}), 404

    if not current_user.organiser or session.organiser_id != current_user.organiser.id:
        return jsonify({"error": "Access forbidden: insufficient permissions."}), 403

    data = request.get_json(silent=True)
    errors = _validate_session_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        session.title = str(data.get("title")).strip()
        session.speaker = str(data.get("speaker")).strip()
        session.track = str(data.get("track")).strip()
        session.room = str(data.get("room")).strip()
        session.start_time = parse_datetime(data.get("start_time"))
        session.end_time = parse_datetime(data.get("end_time"))
        session.capacity = int(data.get("capacity"))
        db.session.commit()
        return jsonify({
            "message": "Session updated successfully.",
            "session": _session_to_public_dict(session),
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def delete_session(session_id):
    session = db.session.get(Session, session_id)
    if not session:
        return jsonify({"error": "Session not found."}), 404

    if not current_user.organiser or session.organiser_id != current_user.organiser.id:
        return jsonify({"error": "Access forbidden: insufficient permissions."}), 403

    try:
        db.session.delete(session)
        db.session.commit()
        return jsonify({"message": "Session deleted successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
