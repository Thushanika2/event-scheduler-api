from datetime import date

from app import create_app
from app.extensions import db
from app.models.agenda_model import Agenda


def seed_agendas():
    app = create_app()
    with app.app_context():
        if Agenda.query.first():
            print("Agendas already exist.")
            return

        agendas = []

        db.session.bulk_save_objects(agendas)
        db.session.commit()
        print(f"Inserted {len(agendas)} agendas.")


if __name__ == "__main__":
    seed_agendas()
