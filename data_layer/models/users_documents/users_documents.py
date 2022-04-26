from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from flask_app import db


class UsersDocuments(db.Model):
    __tablename__ = 'users_documents'

    id = db.Column(db.Integer,
                   primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey("documents.id", ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'))