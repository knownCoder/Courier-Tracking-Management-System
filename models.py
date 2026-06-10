from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    tracking_id = db.Column(db.String(50), unique=True, nullable=False)
    sender_name = db.Column(db.String(100))
    receiver_name = db.Column(db.String(100))

    current_status = db.Column(db.String(50))
    current_location = db.Column(db.String(100))