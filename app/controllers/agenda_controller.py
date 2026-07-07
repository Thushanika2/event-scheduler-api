from flask import jsonify, request
from flask_jwt_extended import current_user

from app.extensions import db
from app.models.agenda_model import AgendaItem
from app.models.session_model import Session


def _sessions_overlap(session_a, session_b):
    return session_a.start_time < session_b.end_time and session_a.end_time > session_b.start_time


def _validate_agenda_payload(data):
    errors = []
    if not data:
        return ["Request body is required."]

    session_id = data.get("session_id")
    if session_id is None:
        errors.append("session_id is required.")
    else:
        session = db.session.get(Session, int(session_id))
        if not session:
            errors.append("session_id does not exist.")

    return errors


def create_agenda_item():
    if not current_user.attendee:
        return jsonify({"error": "Attendee profile not found."}), 404

    data = request.get_json(silent=True)
    errors = _validate_agenda_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    session_id = int(data.get("session_id"))
    session = db.session.get(Session, session_id)
    attendee = current_user.attendee

    existing = AgendaItem.query.filter_by(
        attendee_id=attendee.id,
        session_id=session_id,
    ).first()
    if existing:
        return jsonify({"error": "Session is already in your agenda."}), 400

    enrolled = AgendaItem.query.filter_by(session_id=session_id).count()
    if enrolled >= session.capacity:
        return jsonify({"error": "Session is full."}), 400

    clash_sessions = []
    for item in AgendaItem.query.filter_by(attendee_id=attendee.id).all():
        if item.session and _sessions_overlap(session, item.session):
            clash_sessions.append(item.session.to_dict())

    try:
        agenda_item = AgendaItem(
            attendee_id=attendee.id,
            session_id=session_id,
        )
        db.session.add(agenda_item)
        db.session.commit()

        response = {
            "message": "Session added to agenda.",
            "agenda_item": agenda_item.to_dict(),
        }
        if clash_sessions:
            response["warning"] = "This session overlaps with other sessions in your agenda."
            response["clashing_sessions"] = clash_sessions

        return jsonify(response), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_my_agenda():
    if not current_user.attendee:
        return jsonify({"error": "Attendee profile not found."}), 404

    items = (
        AgendaItem.query.filter_by(attendee_id=current_user.attendee.id)
        .join(Session)
        .order_by(Session.start_time.asc())
        .all()
    )
    return jsonify({"agenda_items": [item.to_dict() for item in items]}), 200


def delete_agenda_item(agenda_item_id):
    if not current_user.attendee:
        return jsonify({"error": "Attendee profile not found."}), 404

    agenda_item = db.session.get(AgendaItem, agenda_item_id)
    if not agenda_item:
        return jsonify({"error": "Agenda item not found."}), 404

    if agenda_item.attendee_id != current_user.attendee.id:
        return jsonify({"error": "Access forbidden: insufficient permissions."}), 403

    try:
        db.session.delete(agenda_item)
        db.session.commit()
        return jsonify({"message": "Agenda item removed successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
