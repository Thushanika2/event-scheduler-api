from datetime import date

from app import create_app
from app.extensions import db
from app.models.session_model import Session


def seed_sessions():
    app = create_app()
    with app.app_context():
        if Session.query.first():
            print("Sessions already exist.")
            return

        sessions = []

        db.session.bulk_save_objects(sessions)
        db.session.commit()
        print(f"Inserted {len(sessions)} sessions.")


if __name__ == "__main__":
    seed_sessions()
