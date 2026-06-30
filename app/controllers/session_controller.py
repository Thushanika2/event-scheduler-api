from datetime import datetime
from flask import jsonify, request
from app.extensions import db
from app.models.session_model import Session

def create_session():
    data = request.get_json(silent=True)
    if not data:
        return jsonify ({"error":"request body is required"}), 400
    
    try:
        session = Session(
            room_id = data.get("room_id"),
            title = data.get("title"),
            speaker = data.get("speaker"),
            date = data.get("date"),
            start_time = data.get("start_time"),
            end_time = data.get("end time"),
            capacity = data.get("capacity")
        )

    except Exception as e:
        db.session.rollback()
        return jsonify ({"error": e})
    
def get_sessions():
    sessions = Session.query.all()
    return jsonify ({"error":[s.to_dict() for s in sessions]}), 200

def get_session(session_id):
    session = Session.query.get(session_id)
    if not session:
        return jsonify({"error": "Session not found."}), 404
    return jsonify({"session": session.to_dict()}), 200

