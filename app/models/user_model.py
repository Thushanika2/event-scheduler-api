from app.extensions import db
from app.utils import utc_now

class User(db.Model):
    __tablename__ = "users"

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    email=db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")
    created_at = db.Column(db.DateTime, default=utc_now)

    def to_dict(self):
        """Return a dictionary representation of the user."""
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
