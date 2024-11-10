# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo
from . import db

def obter_timestamp_brasilia():
    return datetime.now(ZoneInfo('America/Sao_Paulo'))

class DadosSensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperatura = db.Column(db.Float, nullable=False)
    umidade = db.Column(db.Float, nullable=False)
    luminosidade = db.Column(db.Integer, nullable=False) 
    umidadesolo = db.Column(db.Integer, nullable=False)  
    timestamp = db.Column(db.DateTime, default=obter_timestamp_brasilia, nullable=False)