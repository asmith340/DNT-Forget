from flask_sqlalchemy import SQLAlchemy
from app_setup import app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)


class Person(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<Person {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    username = db.Column(db.String(64))
    date = db.Column(db.String(64))
    # folder=db.Column(db.String(64))

    def __repr__(self):
        return "<Title {}>, Date {}".format(self.title, self.date)


class EventText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    username = db.Column(db.String(64))
    text = db.Column(db.String(8000))
    # folder=db.Column(db.String(64))

    def __repr__(self):
        return "<Title {}>, Text {}".format(self.title, self.text)


db.create_all()
