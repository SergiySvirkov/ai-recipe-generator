# app/api/__init__.py
# This file ties all the API routes together.

from flask import Blueprint

api = Blueprint('api', __name__)

# Import all the route modules to register them with the blueprint
from . import auth, generator, recipes
