# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow # Import Marshmallow
from config import config
from app.services.ai_service import RecipeGenerator

# --- Extension Initialization ---
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
ma = Marshmallow() # Initialize Marshmallow

# --- AI Service Initialization ---
recipe_generator = RecipeGenerator()

def create_app(config_name='default'):
    """
    Application factory function.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    ma.init_app(app) # Bind Marshmallow to the app

    # --- Register Blueprints ---
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
