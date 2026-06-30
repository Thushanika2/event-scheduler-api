from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers import room_controller as ctrl

room_bp = Blueprint("rooms", __name__, url_prefix="/api/rooms")

@room_bp.route("", methods=["POST"])
@jwt_required()
def create_room():
    return ctrl.create_room()

@room_bp.route("", methods=["GET"])
@jwt_required()
def get_rooms():
    return ctrl.get_rooms()

@room_bp.route("/<int:room_id>", methods=["GET"])
def get_room(room_id):
    return ctrl.get_room(room_id)

@room_bp.route("/<int:room_id>", methods=["PUT"])
def update_room(room_id):
    return ctrl.update_room(room_id)

@room_bp.route("/<int:room_id>", methods=["DELETE"])
def delete_room(room_id):
    return ctrl.delete_room(room_id)
