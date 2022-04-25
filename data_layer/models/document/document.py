from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from flask_app import db

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.Text)
    text = db.Column(db.Text)
