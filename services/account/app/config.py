import os

SECRET_KEY_DEFAULT = 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw'
SECURITY_PASSWORD_SALT_DEFAULT = '146585145368132386173505678016728509634'

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """Base config, uses staging database server."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Generate a nice key using secrets.token_urlsafe()
    SECRET_KEY = os.environ.get("SECRET_KEY", SECRET_KEY_DEFAULT)

    # Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
    # Generate a good salt using: secrets.SystemRandom().getrandbits(128)
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT',
                                            SECURITY_PASSWORD_SALT_DEFAULT)
    # Specifies the path to the template for the user login page.
    SECURITY_LOGIN_USER_TEMPLATE = 'signin.html'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class ProductionConfig(Config):
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler

        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
