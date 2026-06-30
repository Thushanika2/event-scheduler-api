from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers import agenda_controller as ctrl

agenda_bp = Blueprint("agendas", __name__, url_prefix="/api/agendas")

@agenda_bp.route("", methods=["POST"])
@jwt_required()
def create_agenda():
    return ctrl.create_agenda()

@agenda_bp.route("", methods=["GET"])
@jwt_required()
def get_agendas():
    return ctrl.get_agendas()

@agenda_bp.route("/<int:agenda_id>", methods=["GET"])
def get_agenda(agenda_id):
    return ctrl.get_agenda(agenda_id)

@agenda_bp.route("/<int:agenda_id>", methods=["PUT"])
def update_agenda(agenda_id):
    return ctrl.update_agenda(agenda_id)

@agenda_bp.route("/<int:agenda_id>", methods=["DELETE"])
def delete_agenda(agenda_id):
    return ctrl.delete_agenda(agenda_id)
