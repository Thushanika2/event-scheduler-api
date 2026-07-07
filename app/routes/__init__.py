from app.routes.auth_routes import auth_bp
from app.routes.attendee_routes import attendee_bp
from app.routes.organiser_routes import organiser_bp
from app.routes.session_routes import session_bp, organiser_session_bp
from app.routes.agenda_routes import agenda_bp
from app.routes.admin_routes import admin_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(attendee_bp)
    app.register_blueprint(organiser_bp)
    app.register_blueprint(session_bp)
    app.register_blueprint(organiser_session_bp)
    app.register_blueprint(agenda_bp)
    app.register_blueprint(admin_bp)
