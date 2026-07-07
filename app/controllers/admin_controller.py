from flask import jsonify, request

from app.extensions import db
from app.models.attendee_model import Attendee
from app.models.organiser_model import Organiser
from app.models.user_model import User


def _attendee_admin_dict(attendee):
    user = attendee.user
    return {
        **attendee.to_dict(),
        "email": user.email if user else None,
        "is_active": user.is_active if user else False,
        "created_at": user.created_at.isoformat() if user and user.created_at else None,
    }


def _organiser_admin_dict(organiser):
    user = organiser.user
    return {
        **organiser.to_dict(),
        "email": user.email if user else None,
        "is_active": user.is_active if user else False,
        "created_at": user.created_at.isoformat() if user and user.created_at else None,
    }


def _validate_attendee_admin_payload(data, require_fields=True):
    errors = []
    if not data:
        return ["Request body is required."]

    if require_fields:
        full_name = data.get("full_name")
        if full_name is None or str(full_name).strip() == "":
            errors.append("full_name is required.")

    return errors


def _validate_organiser_admin_payload(data, require_fields=True):
    errors = []
    if not data:
        return ["Request body is required."]

    if require_fields:
        full_name = data.get("full_name")
        if full_name is None or str(full_name).strip() == "":
            errors.append("full_name is required.")

    return errors


def get_attendees():
    attendees = Attendee.query.join(User).order_by(Attendee.id.asc()).all()
    return jsonify({"attendees": [_attendee_admin_dict(a) for a in attendees]}), 200


def get_attendee(attendee_id):
    attendee = db.session.get(Attendee, attendee_id)
    if not attendee:
        return jsonify({"error": "Attendee not found."}), 404
    return jsonify({"attendee": _attendee_admin_dict(attendee)}), 200


def update_attendee(attendee_id):
    attendee = db.session.get(Attendee, attendee_id)
    if not attendee:
        return jsonify({"error": "Attendee not found."}), 404

    data = request.get_json(silent=True)
    errors = _validate_attendee_admin_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        attendee.full_name = str(data.get("full_name")).strip()
        attendee.phone = str(data.get("phone")).strip() if data.get("phone") else None

        if "is_active" in data and attendee.user:
            attendee.user.is_active = bool(data.get("is_active"))

        db.session.commit()
        return jsonify({
            "message": "Attendee updated successfully.",
            "attendee": _attendee_admin_dict(attendee),
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


def approve_attendee(attendee_id):
    attendee = db.session.get(Attendee, attendee_id)
    if not attendee or not attendee.user:
        return jsonify({"error": "Attendee not found."}), 404

    try:
        attendee.user.is_active = True
        db.session.commit()
        return jsonify({
            "message": "Attendee approved successfully.",
            "attendee": _attendee_admin_dict(attendee),
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def disapprove_attendee(attendee_id):
    attendee = db.session.get(Attendee, attendee_id)
    if not attendee or not attendee.user:
        return jsonify({"error": "Attendee not found."}), 404

    try:
        attendee.user.is_active = False
        db.session.commit()
        return jsonify({
            "message": "Attendee disapproved successfully.",
            "attendee": _attendee_admin_dict(attendee),
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_organisers():
    organisers = Organiser.query.join(User).order_by(Organiser.id.asc()).all()
    return jsonify({"organisers": [_organiser_admin_dict(o) for o in organisers]}), 200


def get_organiser(organiser_id):
    organiser = db.session.get(Organiser, organiser_id)
    if not organiser:
        return jsonify({"error": "Organiser not found."}), 404
    return jsonify({"organiser": _organiser_admin_dict(organiser)}), 200


def update_organiser(organiser_id):
    organiser = db.session.get(Organiser, organiser_id)
    if not organiser:
        return jsonify({"error": "Organiser not found."}), 404

    data = request.get_json(silent=True)
    errors = _validate_organiser_admin_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        organiser.full_name = str(data.get("full_name")).strip()
        organiser.organisation = (
            str(data.get("organisation")).strip() if data.get("organisation") else None
        )
        organiser.phone = str(data.get("phone")).strip() if data.get("phone") else None

        if "is_active" in data and organiser.user:
            organiser.user.is_active = bool(data.get("is_active"))

        db.session.commit()
        return jsonify({
            "message": "Organiser updated successfully.",
            "organiser": _organiser_admin_dict(organiser),
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


def approve_organiser(organiser_id):
    organiser = db.session.get(Organiser, organiser_id)
    if not organiser or not organiser.user:
        return jsonify({"error": "Organiser not found."}), 404

    try:
        organiser.user.is_active = True
        db.session.commit()
        return jsonify({
            "message": "Organiser approved successfully.",
            "organiser": _organiser_admin_dict(organiser),
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def disapprove_organiser(organiser_id):
    organiser = db.session.get(Organiser, organiser_id)
    if not organiser or not organiser.user:
        return jsonify({"error": "Organiser not found."}), 404

    try:
        organiser.user.is_active = False
        db.session.commit()
        return jsonify({
            "message": "Organiser disapproved successfully.",
            "organiser": _organiser_admin_dict(organiser),
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_stats():
    pending_attendees = (
        Attendee.query.join(User).filter(User.is_active.is_(False)).count()
    )
    pending_organisers = (
        Organiser.query.join(User).filter(User.is_active.is_(False)).count()
    )

    from app.models.session_model import Session

    return jsonify({
        "stats": {
            "attendees": Attendee.query.count(),
            "organisers": Organiser.query.count(),
            "sessions": Session.query.count(),
            "pending_attendees": pending_attendees,
            "pending_organisers": pending_organisers,
        },
    }), 200
