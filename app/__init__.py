import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config


db = SQLAlchemy()
bootstrap = Bootstrap()
migrate = Migrate()
login = LoginManager()

login.login_view = "auth.login"  # type: ignore


@login.user_loader
def load_user(user_id):
    from app.models import Users

    return Users.query.get(int(user_id))


def create_app(config_type=None):
    if config_type is None:
        config_type = "development"
    app = Flask(__name__)

    app.config.from_object(config[config_type])

    db.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from .blueprints import main_bp, auth_bp, task_bp, profile_bp, users_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(task_bp, url_prefix="/task")
    app.register_blueprint(profile_bp, url_prefix="/profile")

    with app.app_context():
        db.create_all()

    return app


app = create_app()
