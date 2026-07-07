from app.extensions import db
from app.models.agenda_model import AgendaItem
from app.models.session_model import Session
from app.seeders.user_seeder import get_seed_user


def seed_agendas():
    if AgendaItem.query.first():
        print("Agenda items already exist.")
        return

    attendee1 = get_seed_user("attendee1@eventscheduler.com")
    attendee2 = get_seed_user("attendee2@eventscheduler.com")

    if not attendee1 or not attendee2:
        print("Attendee seed users missing. Run user seeder first.")
        return

    sessions = Session.query.order_by(Session.start_time.asc()).all()
    if len(sessions) < 3:
        print("Session seed data missing. Run session seeder first.")
        return

    intro_ai = sessions[0]
    ml_workshop = sessions[1]
    cloud_native = sessions[2]
    zero_trust = sessions[4] if len(sessions) > 4 else sessions[-1]

    agenda_items = [
        AgendaItem(attendee_id=attendee1.attendee.id, session_id=intro_ai.id),
        AgendaItem(attendee_id=attendee1.attendee.id, session_id=ml_workshop.id),
        AgendaItem(attendee_id=attendee1.attendee.id, session_id=cloud_native.id),
        AgendaItem(attendee_id=attendee2.attendee.id, session_id=zero_trust.id),
    ]

    db.session.add_all(agenda_items)
    db.session.commit()
    print(f"Seeded {len(agenda_items)} agenda items.")
