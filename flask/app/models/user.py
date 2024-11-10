# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo
from flask_login import UserMixin
from . import db

def obter_timestamp_brasilia():
    return datetime.now(ZoneInfo('America/Sao_Paulo'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'admin', 'student', 'teacher'
    created_at = db.Column(db.DateTime, default=obter_timestamp_brasilia)  # Data de criação