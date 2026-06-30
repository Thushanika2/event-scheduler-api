from datetime import datetime
from flask import jsonify, request
from app.extensions import db
from app.models.agenda_model import Agenda

def create_agenda():
    data = request.get_json(silent=True)
    if not data:
        return jsonify ({"error":"request body is required"}), 400
    
    try:
        agenda = Agenda(
            user_id = data.get("user_id"),
            session_id = data.get("session_id")
        )

    except Exception as e:
        db.session.rollback()
        return jsonify ({"error": e})
    
def get_agendas():
    agendas = Agenda.query.all()
    return jsonify ({"error":[a.to_dict() for a in agendas]}), 200

def get_agenda(agenda_id):
    agenda = Agenda.query.get(agenda_id)
    if not agenda:
        return jsonify({"error": "Agenda not found."}), 404
    return jsonify({"agenda": agenda.to_dict()}), 200

def update_agenda(agenda_id):
    agenda = Agenda.query.get(agenda_id)
    if not agenda:
        return jsonify({"error": "Agenda not found."}), 404
    
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided to update."}), 400
    
    try:
        agenda.user_id = data.get("user_id")
        agenda.agenda_id = data.get("agenda_id")
        db.session.commit()
        return jsonify ({"message":"Agenda update successfully ", "agenda":agenda.to_dict()}),200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": e})
    
def delete_agenda(agenda_id):
    agenda=Agenda.query.get(agenda_id)
    if not agenda:
        return jsonify({"error":"agenda not found"}),404
    
    try:
        db.agenda.delete(agenda)
        db.agenda.commit()
        return jsonify({"agenda deleted successfully"})

    except Exception as e:
        db.agenda.rollback()
        return jsonify({"error": e})