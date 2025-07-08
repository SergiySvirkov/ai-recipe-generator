# app/models.py

from . import db
import json

# --- Association Table ---
# This is a many-to-many relationship table between recipes and ingredients.
# One recipe can have many ingredients, and one ingredient can be in many recipes.
recipe_ingredient_association = db.Table(
    'recipe_ingredient_association',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
)

class User(db.Model):
    """
    User model for storing user accounts.
    Note: This is for future use, as the MVP does not include user authentication.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    # We will add password hash and other fields later.
    
    # Relationship to recipes created by the user.
    recipes = db.relationship('Recipe', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

class Ingredient(db.Model):
    """
    Ingredient model. Stores unique ingredient names.
    """
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    def __repr__(self):
        return f'<Ingredient {self.name}>'

class DietaryRestriction(db.Model):
    """
    DietaryRestriction model. Stores different types of dietary needs.
    e.g., 'Vegan', 'Vegetarian', 'Gluten-Free'.
    """
    __tablename__ = 'dietary_restrictions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return f'<DietaryRestriction {self.name}>'

class Recipe(db.Model):
    """
    Recipe model. This is the central model of our application.
    """
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    
    # Instructions are stored as a JSON string for simplicity.
    # A more complex design might use a separate Instructions table.
    instructions_json = db.Column(db.Text, nullable=False)
    
    # Foreign key to link to the user who created the recipe.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Many-to-many relationship with ingredients.
    ingredients = db.relationship(
        'Ingredient', 
        secondary=recipe_ingredient_association,
        backref=db.backref('recipes', lazy='dynamic'),
        lazy='dynamic'
    )

    @property
    def instructions(self):
        """Property to get instructions as a Python list."""
        return json.loads(self.instructions_json)

    @instructions.setter
    def instructions(self, value):
        """Property to set instructions from a Python list to a JSON string."""
        self.instructions_json = json.dumps(value)

    def __repr__(self):
        return f'<Recipe {self.title}>'
