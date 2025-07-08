# Handles user registration and login.

import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app
from . import api
from .. import db
from ..models import User
from .schemas import user_registration_schema
from marshmallow import ValidationError

def token_required(f):
    """Decorator to protect routes with JWT authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['id'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

@api.route('/users/register', methods=['POST'])
def register():
    """Endpoint to register a new user with validation."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400
    
    try:
        # Validate input data
        data = user_registration_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "messages": err.messages}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 409

    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'New user created!'}), 201
    
@api.route('/users/login', methods=['POST'])
def login():
    """Endpoint to log in a user and return a JWT."""
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic realm="Login required!"'}), 401
        
    user = User.query.filter_by(username=auth.username).first()
    if not user or not user.verify_password(auth.password):
        return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic realm="Login required!"'}), 401
        
    token = jwt.encode({
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, current_app.config['JWT_SECRET_KEY'], algorithm="HS256")
    
    return jsonify({'token': token})
