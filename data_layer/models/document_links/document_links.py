from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from flask_app import db

class DocumentLinks(db.Model):
    __tablename__ = 'document_links'

    id = db.Column(db.Integer,
                   primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_used = db.Column(db.Boolean)
    hash = db.Column(db.Text)