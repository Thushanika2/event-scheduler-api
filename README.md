Student API — Flask + MySQL CRUD

REST API built with Flask, SQLAlchemy ORM, and MySQL. Manages Event and agenda with full CRUD operations.

# Setup

in your terminal

Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

Install dependencies
pip install -r requirements.txt

# 3. Create a .env

and update with the information from .env.example

# 4. Create the database in MySQL

mysql -u root -p -e "CREATE DATABASE student_db;"

# 5. Run the app (tables are created automatically on first start)

python run.py

# Environment Variables (`.env`)

| Variable      | Description       | Default     |
| ------------- | ----------------- | ----------- |
| `DB_USER`     | MySQL username    | `root`      |
| `DB_PASSWORD` | MySQL password    | `root123`   |
| `DB_HOST`     | MySQL host        | `localhost` |
| `DB_NAME`     | Database name     | `event_db`  |
| `FLASK_DEBUG` | Enable debug mode | `True`      |

# API Testing

Base URL: `http://localhost:5000`
