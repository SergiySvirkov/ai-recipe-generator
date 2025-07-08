# app/models.py
from . import db
import json
from flask_bcrypt import Bcrypt

# Initialize bcrypt here or within the app factory
bcrypt = Bcrypt()

class User(db.Model):
    """
    Updated User model with password hashing.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    recipes = db.relationship('Recipe', backref='author', lazy='dynamic')

    @property
    def password(self):
        """Prevent password from being accessed"""
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Set password to a hashed password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Check if hashed password matches actual password"""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# --- Other models (Recipe, Ingredient, etc.) remain the same ---
class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

recipe_ingredient_association = db.Table(
    'recipe_ingredient_association',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
)

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    instructions_json = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    ingredients = db.relationship(
        'Ingredient', 
        secondary=recipe_ingredient_association,
        backref=db.backref('recipes', lazy='dynamic'),
        lazy='dynamic'
    )

    @property
    def instructions(self):
        return json.loads(self.instructions_json)

    @instructions.setter
    def instructions(self, value):
        self.instructions_json = json.dumps(value)
