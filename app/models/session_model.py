from app.extensions import db
from app.utils import utc_now

class Session(db.Model):
    __tablename__="sessions"
    session_id = db.Column( db.Integer, primary_key=True, autoincrement=True )
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    title = db.Column( db.String, nullable=False )
    speaker = db.Column( db.String, nullable=False )
    date = db.Column( db.Date, nullable=False )
    start_time = db.Column( db.Time, nullable=False )
    end_time = db.Column( db.Time, nullable=False )
    capacity = db.Column( db.Integer, nullable=False )

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "room_id": self.room_id,
            "title": self.title,
            "speaker": self.speaker,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "capacity": self.capacity,
        }




