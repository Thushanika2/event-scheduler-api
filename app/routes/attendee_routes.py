from flask import Blueprint

from app.controllers import attendee_controller as ctrl
from app.middleware import attendee_owner_required

attendee_bp = Blueprint("attendees", __name__, url_prefix="/api/attendees")


@attendee_bp.route("", methods=["POST"])
def create_attendee():
    return ctrl.create_attendee()


@attendee_bp.route("/<int:attendee_id>", methods=["GET"])
@attendee_owner_required
def get_attendee(attendee_id):
    return ctrl.get_attendee(attendee_id)


@attendee_bp.route("/<int:attendee_id>", methods=["PUT"])
@attendee_owner_required
def update_attendee(attendee_id):
    return ctrl.update_attendee(attendee_id)


@attendee_bp.route("/<int:attendee_id>", methods=["DELETE"])
@attendee_owner_required
def delete_attendee(attendee_id):
    return ctrl.delete_attendee(attendee_id)
