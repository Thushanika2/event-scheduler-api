from app.extensions import db
from app.utils import utc_now


class AgendaItem(db.Model):
    __tablename__ = "agenda_items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attendee_id = db.Column(db.Integer, db.ForeignKey("attendees.id"), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False)
    added_at = db.Column(db.DateTime, default=utc_now)

    attendee = db.relationship("Attendee", back_populates="agenda_items")
    session = db.relationship("Session", back_populates="agenda_items")

    def to_dict(self):
        return {
            "id": self.id,
            "attendee_id": self.attendee_id,
            "session_id": self.session_id,
            "added_at": self.added_at.isoformat() if self.added_at else None,
            "session": self.session.to_dict() if self.session else None,
        }
