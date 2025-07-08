# Handles saving and retrieving recipes for authenticated users.
from flask import request, jsonify
from . import api
from .. import db
from ..models import Recipe, Ingredient
from .auth import token_required
from .schemas import save_recipe_schema
from marshmallow import ValidationError

@api.route('/recipes', methods=['POST'])
@token_required
def save_recipe(current_user):
    """Endpoint to save a new recipe with validation."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400
        
    try:
        data = save_recipe_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "messages": err.messages}), 400

    new_recipe = Recipe(
        title=data['title'], 
        instructions=data['instructions'], 
        author=current_user
    )
    # ... (rest of the logic remains the same)
    for ing_name in data['ingredients']:
        ingredient = Ingredient.query.filter_by(name=ing_name).first()
        if not ingredient:
            ingredient = Ingredient(name=ing_name)
            db.session.add(ingredient)
        new_recipe.ingredients.add(ingredient)

    db.session.add(new_recipe)
    db.session.commit()

    return jsonify({'message': 'Recipe saved!', 'id': new_recipe.id}), 201

@api.route('/recipes', methods=['GET'])
@token_required
def get_recipes(current_user):
    """Endpoint to get all recipes saved by the logged-in user."""
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    output = []
    for recipe in recipes:
        recipe_data = {
            'id': recipe.id,
            'title': recipe.title,
            'ingredients': [ing.name for ing in recipe.ingredients],
            'instructions': recipe.instructions
        }
        output.append(recipe_data)
        
    return jsonify({'recipes': output})
