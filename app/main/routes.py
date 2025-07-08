# app/main/routes.py

from flask import jsonify
from . import main

@main.route('/')
def index():
    """
    Root endpoint to act as a health check.
    It confirms that the server is running.
    """
    return jsonify({
        "status": "ok",
        "message": "Welcome to the AI Recipe Generator API!"
    })
