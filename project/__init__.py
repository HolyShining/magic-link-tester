from os import environ

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .aes_cipher import AESCipher

db = SQLAlchemy()
cipher = None


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    global cipher
    cipher = AESCipher(app.config["SECRET_KEY"])
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login_await"

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    db.init_app(app)

    from project.views.auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    from project.views.main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from project.views.monitoring import monitoring as monitoring_blueprint

    app.register_blueprint(monitoring_blueprint)

    from project.views.tokens import tokens as tokens_blueprint

    app.register_blueprint(tokens_blueprint)

    return app
