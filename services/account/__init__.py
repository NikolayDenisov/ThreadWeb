# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# import os
# from flask_login import LoginManager
# from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
# from flask_security.models import fsqla_v3 as fsqla
#
# db = SQLAlchemy()
#
# # Define models
# fsqla.FsModels.set_db_info(db)
#
# def create_app():
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
#     app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
#     app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT",
#                                                           '257177686643993327101624274978798672711')
#     app.config['SECURITY_PASSWORD_SINGLE_HASH'] = 'False'
#     app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
#     app.config["SESSION_COOKIE_SAMESITE"] = "strict"
#
#     app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
#         "pool_pre_ping": True,
#     }
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite://')
#     db.init_app(app)
#
#     login_manager = LoginManager()
#     login_manager.login_view = 'auth.login'
#     login_manager.init_app(app)
#     from .models import User
#     @login_manager.user_loader
#     def load_user(user_id):
#         # since the user_id is just the primary key of our user table, use it in the query for the user
#         return User.query.get(int(user_id))
#
#     from .routes import auth as auth_blueprint
#     app.register_blueprint(auth_blueprint)
#
#     # Setup Flask-Security
#     user_datastore = SQLAlchemyUserDatastore(db, User, Role)
#     app.security = Security(app, user_datastore)
#     return app
#
#
# if __name__ == '__main__':
#     app = create_app()
#     app.run(DEBUG=True)


import os

from flask import Flask
from flask_security import Security, hash_password, SQLAlchemySessionUserDatastore
from database import db_session, init_db
from models import User, Role


def create_app():
    # Create app
    app = Flask(__name__)
    app.config['DEBUG'] = True

    # Generate a nice key using secrets.token_urlsafe()
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
    # Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
    # Generate a good salt using: secrets.SystemRandom().getrandbits(128)
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
    app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
    # Specifies the path to the template for the user login page.
    app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'signin.html'
    # Setup Flask-Security
    user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
    app.security = Security(app, user_datastore)

    from routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Create a user to test with
        init_db()
        if not app.security.datastore.find_user(email="test@me.com"):
            app.security.datastore.create_user(email="test@me.com", password=hash_password("password"))
        db_session.commit()
    app.run()