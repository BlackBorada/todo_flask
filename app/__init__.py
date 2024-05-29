from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import POSTGRESQL_DATABASE_URI



db = SQLAlchemy()
bootstrap = Bootstrap()
migrate = Migrate()
login = LoginManager()

login.login_view = 'auth.login' # type: ignore

@login.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRESQL_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "secret_key_for_flask_app"
    # Initialize Flask extensions with the app instance
    db.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from .blueprints import main_bp, auth_bp, task_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(task_bp, url_prefix="/task")

    with app.app_context():
        db.create_all()


    return app

app = create_app()
