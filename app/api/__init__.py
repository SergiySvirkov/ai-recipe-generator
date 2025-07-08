# app/api/__init__.py

from flask import Blueprint

# Create a Blueprint object. 
# The first argument, 'api', is the name of the blueprint.
# The second argument, __name__, helps Flask locate the blueprint's resources.
api = Blueprint('api', __name__)

# Import the routes at the end to avoid circular dependencies.
from . import routes
