from __future__ import annotations
from . import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


class Users(db.Model):
    __tablename__ = 'users'

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), unique=False)
    registration_date = db.Column(db.Date, unique=False)

    def __init__(self, name, password, registration_date):
        self.name, self.password, self.registration_date = name, password, registration_date


class Notes(db.Model):
    __tablename__ = 'notes'

    _id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(80), unique=False)
    date = db.Column(db.Date, unique=False)
    user_id = db.Column(db.Integer, ForeignKey('users._id'))
    user = relationship("Users", backref=backref('notes', order_by=_id))

    def __init__(self, note, date):
        self.note, self.date = note, date
