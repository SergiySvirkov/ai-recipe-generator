# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS # Import CORS
from config import config
from app.services.ai_service import RecipeGenerator

# --- Extension Initialization ---
db = SQLAlchemy()
migrate = Migrate()
# Initialize CORS but do not attach it to the app yet.
cors = CORS()

# --- AI Service Initialization ---
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
    
    # Initialize CORS for the app.
    # This will allow our React frontend (running on a different port/domain)
    # to make requests to the API. We restrict it to the /api/ path.
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}}) # For development, allow all origins.
    
    # --- Register Blueprints ---
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
