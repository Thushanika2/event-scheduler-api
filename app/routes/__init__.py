from app.routes.auth_routes import auth_bp
from app.routes.session_routes import session_bp
from app.routes.room_routes import room_bp
from app.routes.agenda_routes import agenda_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(session_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(agenda_bp)



