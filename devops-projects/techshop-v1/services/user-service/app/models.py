import uuid
from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'

    id         = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email      = db.Column(db.String(255), unique=True, nullable=False)
    name       = db.Column(db.String(255), nullable=False)
    password   = db.Column(db.String(255), nullable=False)  # bcrypt hash
    created_at = db.Column(db.DateTime, default=datetime.utcnow)