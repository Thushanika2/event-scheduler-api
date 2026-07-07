from datetime import timedelta

from app.extensions import db
from app.models.session_model import Session
from app.seeders.user_seeder import CONFERENCE_DAY, get_seed_user


def seed_sessions():
    if Session.query.first():
        print("Sessions already exist.")
        return

    organiser1 = get_seed_user("organiser1@eventscheduler.com")
    organiser2 = get_seed_user("organiser2@eventscheduler.com")

    if not organiser1 or not organiser2:
        print("Organiser seed users missing. Run user seeder first.")
        return

    sessions = [
        Session(
            organiser_id=organiser1.organiser.id,
            title="Introduction to AI",
            speaker="Dr. Priya Nair",
            track="AI",
            room="Hall A",
            start_time=CONFERENCE_DAY.replace(hour=9, minute=0),
            end_time=CONFERENCE_DAY.replace(hour=10, minute=0),
            capacity=50,
        ),
        Session(
            organiser_id=organiser1.organiser.id,
            title="Machine Learning Workshop",
            speaker="Dr. Priya Nair",
            track="AI",
            room="Hall B",
            start_time=CONFERENCE_DAY.replace(hour=9, minute=30),
            end_time=CONFERENCE_DAY.replace(hour=10, minute=30),
            capacity=40,
        ),
        Session(
            organiser_id=organiser1.organiser.id,
            title="Building Cloud Native Apps",
            speaker="Alex Chen",
            track="Cloud",
            room="Hall C",
            start_time=CONFERENCE_DAY.replace(hour=11, minute=0),
            end_time=CONFERENCE_DAY.replace(hour=12, minute=0),
            capacity=60,
        ),
        Session(
            organiser_id=organiser2.organiser.id,
            title="Kubernetes Deep Dive",
            speaker="Sam Taylor",
            track="Cloud",
            room="Room 201",
            start_time=CONFERENCE_DAY.replace(hour=13, minute=0),
            end_time=CONFERENCE_DAY.replace(hour=14, minute=0),
            capacity=35,
        ),
        Session(
            organiser_id=organiser2.organiser.id,
            title="Zero Trust Security",
            speaker="Morgan Blake",
            track="Security",
            room="Room 202",
            start_time=CONFERENCE_DAY.replace(hour=14, minute=0),
            end_time=CONFERENCE_DAY.replace(hour=15, minute=0),
            capacity=2,
        ),
        Session(
            organiser_id=organiser2.organiser.id,
            title="API Security Best Practices",
            speaker="Morgan Blake",
            track="Security",
            room="Room 203",
            start_time=CONFERENCE_DAY.replace(hour=15, minute=0),
            end_time=CONFERENCE_DAY.replace(hour=16, minute=0),
            capacity=45,
        ),
        Session(
            organiser_id=organiser2.organiser.id,
            title="Future of Event Platforms",
            speaker="Sam Taylor",
            track="Cloud",
            room="Main Stage",
            start_time=CONFERENCE_DAY + timedelta(days=1, hours=9),
            end_time=CONFERENCE_DAY + timedelta(days=1, hours=10),
            capacity=100,
        ),
    ]

    db.session.add_all(sessions)
    db.session.commit()
    print(f"Seeded {len(sessions)} sessions.")
