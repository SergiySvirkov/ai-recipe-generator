from flask import request, jsonify
from . import api
from .. import recipe_generator
from .schemas import generate_recipe_schema
from marshmallow import ValidationError

@api.route('/generate-recipe', methods=['POST'])
def generate_recipe_endpoint():
    """API endpoint to generate a recipe with validation."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400
        
    try:
        data = generate_recipe_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "messages": err.messages}), 400

    try:
        generated_recipe = recipe_generator.generate(data['ingredients'], data['diet'])
        return jsonify(generated_recipe), 200
    except Exception as e:
        print(f"An error occurred during recipe generation: {e}")
        return jsonify({"error": "Failed to generate recipe"}), 500
