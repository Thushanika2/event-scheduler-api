from app.extensions import db

class Room(db.Model):
    __tablename__ = "rooms"

    agenda_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))

     

    def to_dict(self):
        return {
            "agenda_id":self.agenda_id ,
            "user_id": self.user_id,
            "session_id": self.session_id,
        }
