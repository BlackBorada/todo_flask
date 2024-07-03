from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask.views import MethodView

from app import db
from app.forms import RegistrationForm, LoginForm
from app.models import Users


# TODO rewrite to Class-based Views

auth_bp = Blueprint("auth", __name__)


class RegistrationView(MethodView):
    def get(self):
        form = RegistrationForm()
        return render_template(
            "auth/registration.html", title="Registration", form=form
        )

    def post(self):
        form = RegistrationForm()
        if form.validate_on_submit():
            existing_username = Users.query.filter_by(
                username=form.username.data
            ).first()
            if existing_username is not None:
                flash("Username already exists")
                return redirect(url_for("auth.registration"))

            existing_email = Users.query.filter_by(email=form.email.data).first()
            if existing_email is not None:
                flash("Email already exists")
                return redirect(url_for("auth.registration"))

            user = Users(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )
            db.session.add(user)
            db.session.commit()
            flash("Registration on ready.")
            return redirect(url_for("auth.login"))
        return render_template(
            "auth/registration.html", title="Registration", form=form
        )


class LoginView(MethodView):
    def get(self):
        form = LoginForm()
        return render_template("auth/login.html", title="Sign In", form=form)

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("Invalid username or password")
                return redirect(url_for("auth.login"))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("index.index"))
        return render_template("auth/login.html", title="Sign In", form=form)


class LogoutView(MethodView):
    def get(self):
        logout_user()
        return redirect(url_for("index.index"))


auth_bp.add_url_rule(
    "/registration", view_func=RegistrationView.as_view("registration")
)
auth_bp.add_url_rule("/login", view_func=LoginView.as_view("login"))
auth_bp.add_url_rule("/logout", view_func=LogoutView.as_view("logout"))
