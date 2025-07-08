# app/main/__init__.py

from flask import Blueprint

# This blueprint will handle non-API routes, like a simple health check.
main = Blueprint('main', __name__)

# Import routes at the end to avoid circular dependencies
from . import routes
