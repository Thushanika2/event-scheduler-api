from datetime import date

from app import create_app
from app.extensions import db
from app.models.room_model import Room


def seed_rooms():
    app = create_app()
    with app.app_context():
        if Room.query.first():
            print("Rooms already exist.")
            return

        rooms = []

        db.session.bulk_save_objects(rooms)
        db.session.commit()
        print(f"Inserted {len(rooms)} rooms.")


if __name__ == "__main__":
    seed_rooms()
