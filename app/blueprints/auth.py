from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.forms import RegistrationForm, LoginForm
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/profile")
@login_required
def profile():
    return render_template("auth/profile.html", title="Profile", user=current_user)


# TODO: change the register on registration
# TODO: Add check a duplicate in username and emails in database on registration
@auth_bp.route("/registratoin", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_username = User.query.filter_by(username=form.username.data).first()
        if existing_username is not None:
            flash("Username already exists")
            return redirect(url_for("auth.registratoin"))

        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email is not None:
            flash("Email already exists")
            return redirect(url_for("auth.registratoin"))

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration on ready.")
        return redirect(url_for("auth.login"))
    return render_template("auth/registration.html", title="Registration", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index.index"))
    return render_template("auth/login.html", title="Sign In", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index.index"))
