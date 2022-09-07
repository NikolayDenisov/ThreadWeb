from flask import Flask
from flask_security import Security, SQLAlchemySessionUserDatastore
from .config import DevelopmentConfig

from .database import db_session, init_db
from .models import User, Role

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
app.security = Security(app, user_datastore)
from .routes import auth as auth_blueprint
app.register_blueprint(auth_blueprint)
# if __name__ == '__main__':
#     app = create_app()
#     print('TYTY')
#     with app.app_context():
#         # Create a user to test with
#         init_db()
#         if not app.security.datastore.find_user(email="test@me.com"):
#             app.security.datastore.create_user(email="test@me.com", password=hash_password("password"))
#         db_session.commit()
#     app.run()
