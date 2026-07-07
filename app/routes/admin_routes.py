from flask import Blueprint

from app.controllers import admin_controller as ctrl
from app.middleware import jwt_required_user, roles_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.route("/stats", methods=["GET"])
@jwt_required_user
@roles_required("admin")
def get_stats():
    return ctrl.get_stats()


@admin_bp.route("/attendees", methods=["GET"])
@jwt_required_user
@roles_required("admin")
def get_attendees():
    return ctrl.get_attendees()


@admin_bp.route("/attendees/<int:attendee_id>", methods=["GET"])
@jwt_required_user
@roles_required("admin")
def get_attendee(attendee_id):
    return ctrl.get_attendee(attendee_id)


@admin_bp.route("/attendees/<int:attendee_id>", methods=["PUT"])
@jwt_required_user
@roles_required("admin")
def update_attendee(attendee_id):
    return ctrl.update_attendee(attendee_id)


@admin_bp.route("/attendees/<int:attendee_id>", methods=["DELETE"])
@jwt_required_user
@roles_required("admin")
def delete_attendee(attendee_id):
    return ctrl.delete_attendee(attendee_id)


@admin_bp.route("/attendees/<int:attendee_id>/approve", methods=["POST"])
@jwt_required_user
@roles_required("admin")
def approve_attendee(attendee_id):
    return ctrl.approve_attendee(attendee_id)


@admin_bp.route("/attendees/<int:attendee_id>/disapprove", methods=["POST"])
@jwt_required_user
@roles_required("admin")
def disapprove_attendee(attendee_id):
    return ctrl.disapprove_attendee(attendee_id)


@admin_bp.route("/organisers", methods=["GET"])
@jwt_required_user
@roles_required("admin")
def get_organisers():
    return ctrl.get_organisers()


@admin_bp.route("/organisers/<int:organiser_id>", methods=["GET"])
@jwt_required_user
@roles_required("admin")
def get_organiser(organiser_id):
    return ctrl.get_organiser(organiser_id)


@admin_bp.route("/organisers/<int:organiser_id>", methods=["PUT"])
@jwt_required_user
@roles_required("admin")
def update_organiser(organiser_id):
    return ctrl.update_organiser(organiser_id)


@admin_bp.route("/organisers/<int:organiser_id>", methods=["DELETE"])
@jwt_required_user
@roles_required("admin")
def delete_organiser(organiser_id):
    return ctrl.delete_organiser(organiser_id)


@admin_bp.route("/organisers/<int:organiser_id>/approve", methods=["POST"])
@jwt_required_user
@roles_required("admin")
def approve_organiser(organiser_id):
    return ctrl.approve_organiser(organiser_id)


@admin_bp.route("/organisers/<int:organiser_id>/disapprove", methods=["POST"])
@jwt_required_user
@roles_required("admin")
def disapprove_organiser(organiser_id):
    return ctrl.disapprove_organiser(organiser_id)
