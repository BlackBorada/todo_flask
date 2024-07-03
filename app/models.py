from datetime import datetime

from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.dialects.postgresql import JSONB

import enum


# NOTE: add comments
# NOTE: add tags with tasks
# NOTE   : add role to user


class UserRole(enum.Enum):
    user = "user"
    admin = "admin"


class TaskStatus(enum.Enum):
    pending = "Pending"
    in_progress = "In progress"
    completed = "Completed"
    cancelled = "Cancelled"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.pending)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    settings = db.Column(JSONB)

    tags = db.relationship("Tags", secondary="task_tags", backref="task")

    def __init__(
        self,
        title,
        description=None,
        due_date=None,
        completed=False,
        user_id=None,
        status=TaskStatus.pending,
        **kwargs,
    ):
        self.title = title
        self.description = description
        self.due_date = due_date if due_date is not None else datetime.utcnow()
        self.completed = completed
        self.user_id = user_id
        self.status = status

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"Task('{self.title}', \
        '{self.description}', \
        '{self.due_date}', \
        '{self.completed}')"


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    user_role = db.Column(db.Enum(UserRole), default=UserRole.user)

    tasks = db.relationship("Task", backref="user", lazy=True)
    comments = db.relationship("Comments", backref="user", lazy=True)
    task_history = db.relationship("TaskHistory", backref="user", lazy=True)

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


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100), nullable=False)


class TaskTags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=False)


class TaskHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum(TaskStatus))
    comment = db.Column(db.Text, nullable=True)
