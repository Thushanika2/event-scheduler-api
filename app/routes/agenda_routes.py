from flask import Blueprint

from app.controllers import agenda_controller as ctrl
from app.middleware import jwt_required_user, roles_required

agenda_bp = Blueprint("agenda", __name__, url_prefix="/api/agenda")


@agenda_bp.route("", methods=["POST"])
@jwt_required_user
@roles_required("attendee")
def create_agenda_item():
    return ctrl.create_agenda_item()


@agenda_bp.route("/my", methods=["GET"])
@jwt_required_user
@roles_required("attendee")
def get_my_agenda():
    return ctrl.get_my_agenda()


@agenda_bp.route("/<int:agenda_item_id>", methods=["DELETE"])
@jwt_required_user
@roles_required("attendee")
def delete_agenda_item(agenda_item_id):
    return ctrl.delete_agenda_item(agenda_item_id)
