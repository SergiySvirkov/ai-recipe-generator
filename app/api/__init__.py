# app/api/__init__.py
# We register the error handlers here.

from flask import Blueprint

api = Blueprint('api', __name__)

# Import routes and error handlers to register them with the blueprint
from . import auth, generator, recipes, errors
