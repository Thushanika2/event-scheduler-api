from app.extensions import db

class Agenda(db.Model):
    __tablename__ = "agendas"

    agenda_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id') , nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.session_id') , nullable=False)

     

    def to_dict(self):
        return {
            "agenda_id":self.agenda_id ,
            "user_id": self.user_id,
            "session_id": self.session_id,
        }
