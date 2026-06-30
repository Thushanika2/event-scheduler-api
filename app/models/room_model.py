from app.extensions import db

class Room(db.Model):
    __tablename__ = "rooms"

    room_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_name=db.Column(db.String(120), nullable=False)
     

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "name": self.name,
        }
