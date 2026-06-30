from datetime import datetime
from flask import jsonify, request
from app.extensions import db
from app.models.room_model import Room

def create_room():
    data = request.get_json(silent=True)
    if not data:
        return jsonify ({"error":"request body is required"}), 400

    try:
        room = Room(
            room_id = data.get("room_id"),
            name = data.get("name")
        )

    except Exception as e:
        db.session.rollback()
        return jsonify ({"error": e})

def get_rooms():
    rooms = Room.query.all()
    return jsonify ({"error":[r.to_dict() for r in rooms]}), 200

def get_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found."}), 404
    return jsonify({"room": room.to_dict()}), 200

def update_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found."}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided to update."}), 400

    try:
        room.user_id = data.get("user_id")
        room.room_id = data.get("room_id")
        db.session.commit()
        return jsonify ({"message":"Room update successfully ", "room":room.to_dict()}),200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": e})

def delete_room(room_id):
    room=Room.query.get(room_id)
    if not room:
        return jsonify({"error":"room not found"}),404

    try:
        db.room.delete(room)
        db.room.commit()
        return jsonify({"room deleted successfully"})

    except Exception as e:
        db.room.rollback()
        return jsonify({"error": e})