from datetime import datetime, timezone

PUBLIC_REGISTER_ROLES = ("attendee", "organiser")
ALL_ROLES = ("attendee", "organiser", "admin")


def utc_now():
    return datetime.now(timezone.utc)


def parse_datetime(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    return datetime.fromisoformat(text)
