from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from hashlib import md5
from app.properties import path


db = SQLAlchemy()
ma = Marshmallow()


def create_app(view_all=None):
    app = Flask(__name__)
    encryptor = md5()

    app.permanent_session_lifetime = timedelta(minutes=15)
    app.config['SQLALCHEMY_DATABASE_URI'] = path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = encryptor.digest()

    db.init_app(app)

    app.debug = True

    from .main_api import login_blueprint, logout_blueprint, notepad_blueprint, register_blueprint, add_blueprint, \
        delete_blueprint, view_blueprint

    app.register_blueprint(login_blueprint)
    app.register_blueprint(logout_blueprint)
    app.register_blueprint(notepad_blueprint)
    app.register_blueprint(register_blueprint)
    app.register_blueprint(add_blueprint)
    app.register_blueprint(delete_blueprint)
    app.register_blueprint(view_blueprint)

    return app
