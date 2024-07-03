from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask.views import MethodView

from app import db
from app.models import Users, Task


users_bp = Blueprint("users", __name__)


class UsersView(MethodView):
    def get(self):
        users = Users.query.all()
        for user in users:
            user.tasks_count = len(user.tasks)
            user.completed_count = Task.query.filter_by(
                user_id=user.id, completed=True
            ).count()
        return render_template("users/users.html", users=users)


users_bp.add_url_rule("/", view_func=UsersView.as_view("users"))
