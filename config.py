# config.py
import os

# Get the absolute path of the directory where this file is located.
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Base configuration settings for the Flask application.
    These settings are common across all environments.
    """
    # Secret key is used for session management and other security purposes.
    # It's important to keep this value secret in a production environment.
    # We use an environment variable or a default value for development.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-hard-to-guess-string'

    # Disable SQLAlchemy's event system, which is not needed and adds overhead.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        """
        A hook for any application-specific initialization.
        Currently, it does nothing but can be extended later.
        """
        pass

class DevelopmentConfig(Config):
    """
    Configuration settings for development environment.
    Inherits from the base Config class.
    """
    # Enables debug mode for Flask, which provides a debugger and reloader.
    DEBUG = True
    
    # Specifies the database URI. For development, we use SQLite,
    # a simple file-based database. The database file will be named 'dev.db'
    # and located in the root directory of the project.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'dev.db')

# A dictionary to easily access configuration classes by name.
config = {
    'development': DevelopmentConfig,
    'default': Development_Config
}
