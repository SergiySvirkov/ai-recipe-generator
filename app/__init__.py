# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from app.services.ai_service import RecipeGenerator # Import the generator

# --- Extension Initialization ---
db = SQLAlchemy()
migrate = Migrate()

# --- AI Service Initialization ---
# We create a single instance of the RecipeGenerator here.
# This ensures that the large AI model is loaded into memory only ONCE when the app starts,
# not on every single request, which is crucial for performance.
recipe_generator = RecipeGenerator()

def create_app(config_name='default'):
    """
    Application factory function. It creates and configures the Flask app.
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # --- Register Blueprints ---
    # We will create and register an API blueprint that will use the recipe_generator.
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
