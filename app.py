import os
import json
from flask import jsonify, request, Blueprint, render_template, redirect, url_for, flash
from flask_login.utils import login_required
from flask_login import current_user, login_user, logout_user

from resources import db, LoginForm, RegistrationForm, Person, get_mock_events, Event
from app_setup import app, login_manager

bp = Blueprint("bp", __name__, template_folder="./build")

# Not great practice to keep 2 routes on one method, should change in release
@bp.route('/')
@bp.route('/index')
@login_required
def index():
    DATA = {"current_user": current_user.username}
    # Setting mocked events since we do not have events in db yet
    events = Event.query.filter_by(username=current_user.username).all()
    event_titles = []
    event_dates = []
    for i in range(len(events)):
        event_titles.append(events[i].title)
        event_dates.append(events[i].date)
    DATA['event_titles'] = event_titles
    DATA['event_dates'] = event_dates
    data = json.dumps(DATA)
    return render_template(
        "index.html",
        data=data,
    )

app.register_blueprint(bp)

@login_manager.user_loader
def load_user(id):
    return Person.query.get(int(id))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("bp.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = Person(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("bp.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Person.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("bp.index"))

    return render_template("login.html", title="Sign In", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("bp.index"))

@app.route("/save", methods=["POST"])
def save():
    """
    Receives JSON data from App.js, saves the event information under the current user
    in the database.
    """
    event_dates=[]
    event_titles=[]
    for i in request.json.get("event"):
        event_titles.append(i['title'])
        event_dates.append(i['date'])
    username = current_user.username
    update_db_ids_for_user(username, event_titles, event_dates)
    #TODO: Return new list of events from user
    return {}

def update_db_ids_for_user(user, event_titles, event_dates):
    """
    Updates the DB so that only entries for valid_ids exist in it.
    @param username: the username of the current user
    @param valid_ids: a set of artist IDs that the DB should update itself
        to reflect
    """
    existing_titles = {
        event.title for event in Event.query.filter_by(username=user).all()
    }
    for i in range(len(event_titles)):
        if event_titles[i] in existing_titles:
            event_titles.pop(i)
            event_dates.pop(i)
    for i in range(len(event_titles)):
        db.session.add(Event(title=event_titles[i], username=user, date=event_dates[i]))
    db.session.commit()


if __name__ == "__main__":
    app.run(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
