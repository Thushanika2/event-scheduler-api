import re 
from flask import jsonify, request
from app.models.user_model import User

def _validate_register_payload(data):
    errors = []
    if not data:
        return ["Reguest body is required"]
    
    email=data.get("email")
    if email is None or str(email)=="":
        errors.append("Email is Required")
    
    password=data.get("password")
    if password is None or str(password)=="":
        errors.append("Password is Required")


def validate_register_payload(data):
    errors = []
    if not data:
        errors.append("Email is Required")

    email=data.get("email")
    if email is None or str(email)=="":
        errors.append("Email is Required")
    
    password=data.get("password")
    if password is None or str(password)=="":
        errors.append("Password is Required")

def register():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "error":"request body is required"
        })
    
    try:
        user = User(
            email=str(data.get("email")).strip(),
            role=data.get("role", "student")
        )
        user.set_password(str(data.get("password")))


    except Exception as e:
        return jsonify({"error":e})
    
def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "error":"request body is required"
        })
    
    try:
       email_str=str(data.get("email")).strip()
       user=User.query.filter_by(email=email_str).first()


    except Exception as e:
        return jsonify({"error":e})