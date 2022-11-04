from __future__ import annotations
from . import db, ma
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from flask_marshmallow import fields


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
    note = db.Column(db.String(2000), unique=False)
    date = db.Column(db.Date, unique=False)
    user_id = db.Column(db.Integer, ForeignKey('users._id'))
    user = relationship("Users", backref=backref('notes', order_by=_id))

    def __init__(self, note, date, user_id):
        self.note, self.date, self.user_id = note, date, user_id

    def update(self, modified_note: Notes) -> None:
        self.date = modified_note.date
        self.note = modified_note.note

    @staticmethod
    def create_from_json(json_body: dict) -> Notes:

        return Notes(
            date=json_body['date'],
            note=json_body['note'],
            user_id=json_body['user_id']
        )


class NotesSchema(ma.Schema):
    _id = fields.fields.Integer()
    date = fields.fields.DateTime(format='%d-%m-%y')
    note = fields.fields.Str()
    user_id = fields.fields.Integer()
