from flask import Blueprint

from app.controllers import organiser_controller as ctrl
from app.middleware import organiser_owner_required

organiser_bp = Blueprint("organisers", __name__, url_prefix="/api/organisers")


@organiser_bp.route("", methods=["POST"])
def create_organiser():
    return ctrl.create_organiser()


@organiser_bp.route("/<int:organiser_id>", methods=["GET"])
@organiser_owner_required
def get_organiser(organiser_id):
    return ctrl.get_organiser(organiser_id)


@organiser_bp.route("/<int:organiser_id>", methods=["PUT"])
@organiser_owner_required
def update_organiser(organiser_id):
    return ctrl.update_organiser(organiser_id)


@organiser_bp.route("/<int:organiser_id>", methods=["DELETE"])
@organiser_owner_required
def delete_organiser(organiser_id):
    return ctrl.delete_organiser(organiser_id)
