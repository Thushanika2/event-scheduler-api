from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers import session_controller as ctrl

session_bp = Blueprint("sessions", __name__, url_prefix="/api/sessions")

@session_bp.route("", methods=["POST"])
@jwt_required()
def create_session():
    return ctrl.create_session()

@session_bp.route("", methods=["GET"])
@jwt_required()
def get_sessions():
    return ctrl.get_sessions()

@session_bp.route("/<int:session_id>", methods=["GET"])
def get_session(session_id):
    return ctrl.get_session(session_id)

@session_bp.route("/<int:session_id>", methods=["PUT"])
def update_session(session_id):
    return ctrl.update_session(session_id)

@session_bp.route("/<int:session_id>", methods=["DELETE"])
def delete_session(session_id):
    return ctrl.delete_session(session_id)
