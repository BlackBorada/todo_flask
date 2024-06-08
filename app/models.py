from datetime import datetime

from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    user_id  = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __init__(self, title, description, due_date, completed, user_id):
        self.title = title
        self.description = description
        self.due_date  = due_date
        self.completed  = completed
        self.user_id   = user_id

    def __repr__(self):
        return f"Task('{self.title}', \
        '{self.description}', \
        '{self.due_date}', \
        '{self.completed}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    tasks = db.relationship('Task', backref='owner', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User: {self.username}>"
