from datetime import datetime, timedelta, timezone

from app.extensions import db
from app.models.attendee_model import Attendee
from app.models.organiser_model import Organiser
from app.models.user_model import User

CONFERENCE_DAY = datetime(2026, 8, 15, tzinfo=timezone.utc)

SEED_USERS = [
    {
        "email": "admin@eventscheduler.com",
        "password": "Admin123!",
        "role": "admin",
        "profile": None,
    },
    {
        "email": "organiser1@eventscheduler.com",
        "password": "Organiser123!",
        "role": "organiser",
        "profile": {
            "full_name": "Alex Chen",
            "organisation": "Tech Events Co",
            "phone": "+1-555-0101",
        },
    },
    {
        "email": "organiser2@eventscheduler.com",
        "password": "Organiser123!",
        "role": "organiser",
        "profile": {
            "full_name": "Sam Taylor",
            "organisation": "Cloud Summit",
            "phone": "+1-555-0102",
        },
    },
    {
        "email": "attendee1@eventscheduler.com",
        "password": "Attendee123!",
        "role": "attendee",
        "profile": {
            "full_name": "Jordan Lee",
            "phone": "+1-555-0201",
        },
    },
    {
        "email": "attendee2@eventscheduler.com",
        "password": "Attendee123!",
        "role": "attendee",
        "profile": {
            "full_name": "Casey Morgan",
            "phone": "+1-555-0202",
        },
    },
]


def seed_users():
    created = 0

    for entry in SEED_USERS:
        if User.query.filter_by(email=entry["email"]).first():
            continue

        user = User(email=entry["email"], role=entry["role"])
        user.set_password(entry["password"])
        db.session.add(user)
        db.session.flush()

        profile = entry["profile"]
        if entry["role"] == "organiser" and profile:
            db.session.add(
                Organiser(
                    user_id=user.id,
                    full_name=profile["full_name"],
                    organisation=profile.get("organisation"),
                    phone=profile.get("phone"),
                )
            )
        elif entry["role"] == "attendee" and profile:
            db.session.add(
                Attendee(
                    user_id=user.id,
                    full_name=profile["full_name"],
                    phone=profile.get("phone"),
                )
            )

        created += 1

    if created:
        db.session.commit()

    print(f"Seeded {created} users.")


def get_seed_user(email):
    return User.query.filter_by(email=email).first()
