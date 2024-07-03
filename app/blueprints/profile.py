from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask.views import MethodView

from app import db
from app.forms import RegistrationForm, LoginForm
from app.models import Users, Task


profile_bp = Blueprint("profile", __name__)


class ProfileView(MethodView):
    def get(self, username):
        user = Users.query.filter_by(username=username).first()
        tasks = user.tasks
        return render_template(
            "profile/profile.html", title="Profile", user=user, tasks=tasks
        )


profile_bp.add_url_rule("/<string:username>", view_func=ProfileView.as_view("profile"))
