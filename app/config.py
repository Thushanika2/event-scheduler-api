from datetime import timedelta
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


def _build_database_uri():
    database_url = os.getenv("DATABASE_URL") or os.getenv("MYSQL_URL")
    if database_url:
        if database_url.startswith("mysql://"):
            return database_url.replace("mysql://", "mysql+pymysql://", 1)
        return database_url

    db_user = os.getenv("DB_USER") or os.getenv("MYSQLUSER")
    db_password = os.getenv("DB_PASSWORD") or os.getenv("MYSQLPASSWORD")
    db_host = os.getenv("DB_HOST") or os.getenv("MYSQLHOST")
    db_port = os.getenv("DB_PORT") or os.getenv("MYSQLPORT") or "3306"
    db_name = os.getenv("DB_NAME") or os.getenv("MYSQLDATABASE")

    if not all([db_user, db_password, db_host, db_name]):
        return None

    return (
        f"mysql+pymysql://{quote_plus(db_user)}:{quote_plus(db_password)}"
        f"@{db_host}:{db_port}/{db_name}"
    )


class Config:
    DB_USER = os.getenv("DB_USER") or os.getenv("MYSQLUSER")
    DB_PASSWORD = os.getenv("DB_PASSWORD") or os.getenv("MYSQLPASSWORD")
    DB_HOST = os.getenv("DB_HOST") or os.getenv("MYSQLHOST")
    DB_PORT = os.getenv("DB_PORT") or os.getenv("MYSQLPORT") or "3306"
    DB_NAME = os.getenv("DB_NAME") or os.getenv("MYSQLDATABASE")

    SQLALCHEMY_DATABASE_URI = _build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", "1440"))
    )
