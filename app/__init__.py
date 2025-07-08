# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

# Initialize the SQLAlchemy extension. This object is the gateway to the database.
db = SQLAlchemy()

# Initialize Migrate. This extension handles database schema migrations.
migrate = Migrate()

def create_app(config_name='default'):
    """
    Application factory function. It creates and configures the Flask app.

    Args:
        config_name (str): The name of the configuration to use (e.g., 'development').

    Returns:
        Flask: The configured Flask application instance.
    """
    # Create the Flask application instance.
    app = Flask(__name__)
    
    # Load the configuration from the specified config object.
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Bind the SQLAlchemy and Migrate extensions to the Flask app instance.
    db.init_app(app)
    migrate.init_app(app, db)
    
    # --- Register Blueprints Here ---
    # Example:
    # from .main import main as main_blueprint
    # app.register_blueprint(main_blueprint)

    return app
