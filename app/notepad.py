from models import Notes
from . import db


def add_to_db(new_note: Notes) -> None:
    db.session.add(new_note)
    db.session.commit()


def delete_from_db(note_to_delete: Notes) -> None:
    db.session.delete(note_to_delete)
    db.session.commit()
