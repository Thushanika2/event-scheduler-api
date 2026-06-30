from app.seeders.session_seeder import seed_sessions
from app.seeders.room_seeder import seed_rooms
from app.seeders.agenda_seeder import seed_agendas


def run_all():
    print("Running session seeder...")
    seed_sessions()
    print("Running room seeder...")
    seed_rooms()
    print("Running agenda seeder...")
    seed_agendas()


if __name__ == "__main__":
    run_all()
