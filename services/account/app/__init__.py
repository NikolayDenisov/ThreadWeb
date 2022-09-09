from flask import Flask
from flask_security import Security, SQLAlchemySessionUserDatastore
from .config import DevelopmentConfig

from .database import db_session, init_db
from .models import User, Role


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # Setup Flask-Security
    user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
    app.security = Security(app, user_datastore)
    from .routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app
