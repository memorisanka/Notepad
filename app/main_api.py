from datetime import datetime
from flask import Blueprint, request, render_template, redirect, session, flash, url_for
from . import db
from .models import Users, Notes


login_blueprint = Blueprint("login", __name__)
logout_blueprint = Blueprint("logout", __name__)
notepad_blueprint = Blueprint("notepad", __name__)
register_blueprint = Blueprint("register", __name__)
add_blueprint = Blueprint("add", __name__)
delete_blueprint = Blueprint("delete", __name__)
view_blueprint = Blueprint("view", __name__)


@login_blueprint.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        nickname = request.form["nickname"]
        password = request.form["password"]
        found_user = Users.query.filter_by(name=nickname).first()

        if not found_user:
            flash("Wrong username or you have to register", "warning")
        elif found_user:
            user_password = found_user.password
            if user_password == password:
                session.update({"nick": nickname, "password": password})
                flash("You've been successfully logged in.", "success")
            else:
                flash("Wrong password.", "warning")

    elif request.method == "GET" and "nick" not in session:
        return render_template("login.html")
    elif request.method == "GET" and "nick" in session:
        flash("Already logged in!", "warning")

    return redirect(url_for("notepad.notepad"))


@login_blueprint.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        nickname = request.form["nickname"]
        password = request.form["password"]
        password_repeat = request.form["password2"]
        registration_date = datetime.now()
        found_user = Users.query.filter_by(name=nickname).first()

        if not found_user and password == password_repeat:
            new_user = Users(
                name=nickname, registration_date=registration_date, password=password
            )
            db.session.add(new_user)
            db.session.commit()
            session.update({"nick": nickname, "password": password})
            flash("You've been successfully registered.", "success")
        elif found_user:
            flash("You've been already registered. Please, log in.", "warning")
            return redirect(url_for("login.login"))
        else:
            flash("Ups...something went wrong...", "warning")
            return render_template("register.html")

    elif request.method == "GET" and "nick" not in session:
        return render_template("register.html")
    elif request.method == "GET" and "nick" in session:
        flash("Already logged in!", "warning")

    return redirect(url_for("notepad.notepad"))


@logout_blueprint.route("/logout")
def logout():
    if "nick" in session:
        session.pop("nick", None)
        session.pop("email", None)
        flash("You have been logged out!", "warning")
    else:
        flash("You are not logged in!", "warning")

    return redirect(url_for("login.login"))


@notepad_blueprint.route("/notepad", methods=["POST", "GET"])
def notepad():
    if "nick" in session:
        nickname = session["nick"]
        query = Users.query.filter_by(name=f"{nickname}").first()
        date_of_register = query.registration_date


        return render_template("notepad.html", nickname=nickname)
    else:
        flash("You are not logged in!", "warning")

    return redirect(url_for("login.login"))



@notepad_blueprint.route("/add", methods=["POST", "GET"])
def add():
    return render_template("new_note.html")


# query = Users.query.filter_by(name=f"{nickname}").first()
#             note_date = datetime.now()
#
#             return render_template("notepad.html", nickname=nickname, date=note_date)
#         else:
#             flash("You are not logged in!", "warning")
