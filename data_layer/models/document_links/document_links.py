from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from flask_app import db

class DocumentLinks(db.Model):
    __tablename__ = 'document_links'

    id = db.Column(db.Integer,
                   primary_key=True)
    document_id = db.Column(db.ForeignKey('document.id'))
    created_at = db.Column(db.DateTime(timezone=True))
    updated_at = db.Column(db.DateTime(timezone=True))