# This file contains handlers for common HTTP errors.

from flask import jsonify
from marshmallow import ValidationError
from . import api

def validation_error(e):
    """Handles Marshmallow validation errors."""
    return jsonify({"error": "Validation error", "messages": e.messages}), 400

@api.errorhandler(400)
def bad_request(e):
    """Handles 400 Bad Request errors."""
    return jsonify({"error": "Bad request", "message": str(e)}), 400

@api.errorhandler(404)
def not_found(e):
    """Handles 404 Not Found errors."""
    return jsonify({"error": "Not found", "message": "The requested resource was not found."}), 404

@api.errorhandler(500)
def internal_server_error(e):
    """Handles 500 Internal Server Error."""
    # In a production app, you would log the error here.
    return jsonify({"error": "Internal server error", "message": "An unexpected error occurred."}), 500
