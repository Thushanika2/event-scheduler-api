# Event Scheduler API

Flask REST API with MySQL for event session scheduling, organiser management, and attendee agendas.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and update values.

Create the database:

```bash
mysql -u root -p -e "CREATE DATABASE event_scheduler_db;"
```

Run the API (tables are created automatically):

```bash
python run.py
```

Base URL: `http://127.0.0.1:5000`

## Environment Variables

| Variable | Description |
| --- | --- |
| `DB_USER` | MySQL username |
| `DB_PASSWORD` | MySQL password |
| `DB_HOST` | MySQL host |
| `DB_NAME` | Database name |
| `JWT_SECRET_KEY` | JWT signing secret |
| `JWT_ACCESS_TOKEN_EXPIRES_MINUTES` | Token expiry in minutes |
| `FLASK_DEBUG` | Enable Flask debug mode |

## Seed the database

After creating tables, run seeders to insert demo users, sessions, and agenda data:

```bash
python run_seeders.py
```

### Seeded accounts

| Role | Email | Password |
| --- | --- | --- |
| Admin | `admin@eventscheduler.com` | `Admin123!` |
| Organiser | `organiser1@eventscheduler.com` | `Organiser123!` |
| Organiser | `organiser2@eventscheduler.com` | `Organiser123!` |
| Attendee | `attendee1@eventscheduler.com` | `Attendee123!` |
| Attendee | `attendee2@eventscheduler.com` | `Attendee123!` |

Admin accounts can only be created via seeders — public registration accepts attendee and organiser roles only.

## Key Endpoints

- `POST /api/auth/register` — register attendee or organiser
- `POST /api/auth/login` — login and receive JWT
- `GET /api/sessions` — public session list (filter by `track`, `start_after`, `start_before`)
- `POST /api/agenda` — attendee adds session to personal agenda (clash warning on overlap)
- `GET /api/admin/stats` — admin dashboard stats
- `GET /api/admin/attendees` — list all attendees (admin)
- `PUT /api/admin/attendees/:id` — edit attendee (admin)
- `DELETE /api/admin/attendees/:id` — delete attendee (admin)
- `POST /api/admin/attendees/:id/approve` — approve attendee (admin)
- `POST /api/admin/attendees/:id/disapprove` — disapprove attendee (admin)
- Same routes under `/api/admin/organisers`
