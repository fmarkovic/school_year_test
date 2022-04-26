from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from flask_app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    username = db.Column(db.Text)
    password = db.Column(db.Text)