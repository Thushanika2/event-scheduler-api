from flask import Blueprint

from app.controllers import session_controller as ctrl
from app.middleware import jwt_required_user, roles_required

session_bp = Blueprint("sessions", __name__, url_prefix="/api/sessions")
organiser_session_bp = Blueprint("organiser_sessions", __name__, url_prefix="/api/organiser")


@session_bp.route("", methods=["GET"])
def get_sessions():
    return ctrl.get_sessions()


@session_bp.route("/<int:session_id>", methods=["GET"])
def get_session(session_id):
    return ctrl.get_session(session_id)


@session_bp.route("", methods=["POST"])
@jwt_required_user
@roles_required("organiser")
def create_session():
    return ctrl.create_session()


@session_bp.route("/<int:session_id>", methods=["PUT"])
@jwt_required_user
@roles_required("organiser")
def update_session(session_id):
    return ctrl.update_session(session_id)


@session_bp.route("/<int:session_id>", methods=["DELETE"])
@jwt_required_user
@roles_required("organiser")
def delete_session(session_id):
    return ctrl.delete_session(session_id)


@organiser_session_bp.route("/sessions", methods=["GET"])
@jwt_required_user
@roles_required("organiser")
def get_organiser_sessions():
    return ctrl.get_organiser_sessions()
