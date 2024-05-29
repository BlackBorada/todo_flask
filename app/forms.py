from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    BooleanField,
    DateTimeField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo


class TaskForm(FlaskForm):
    title = StringField("Title:", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Description:")
    due_date = DateTimeField(
        "Due Date:", format="%Y-%m-%d", validators=[DataRequired()]
    )
    completed = BooleanField("Completed:")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")
