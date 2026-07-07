from app.seeders.user_seeder import seed_users
from app.seeders.session_seeder import seed_sessions
from app.seeders.agenda_seeder import seed_agendas


def run_all():
    print("Running user seeder...")
    seed_users()
    print("Running session seeder...")
    seed_sessions()
    print("Running agenda seeder...")
    seed_agendas()
    print("All seeders completed.")


if __name__ == "__main__":
    from app import create_app

    app = create_app()
    with app.app_context():
        from app.extensions import db

        db.create_all()
        run_all()
