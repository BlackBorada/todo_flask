from flask import Blueprint, render_template

from .auth import auth_bp
from .task import task_bp
from .profile import profile_bp
from .users import users_bp


def create_blueprint():
    blueprint = Blueprint("index", __name__)

    @blueprint.route("/")
    def index():
        return render_template("index.html")

    return blueprint


main_bp = create_blueprint()
