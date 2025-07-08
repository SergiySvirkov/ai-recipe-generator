# app/api/schemas.py

from marshmallow import Schema, fields, validate

class UserRegistrationSchema(Schema):
    """
    Schema for validating user registration data.
    """
    username = fields.Str(required=True, validate=validate.Length(min=3, max=64))
    password = fields.Str(required=True, validate=validate.Length(min=8, max=128))

class GenerateRecipeSchema(Schema):
    """
    Schema for validating the input for recipe generation.
    """
    ingredients = fields.List(
        fields.Str(), 
        required=True, 
        validate=validate.Length(min=1, error="At least one ingredient is required.")
    )
    diet = fields.Str(required=False, missing='any') # 'missing' provides a default value

class SaveRecipeSchema(Schema):
    """
    Schema for validating the data for saving a recipe.
    """
    title = fields.Str(required=True, validate=validate.Length(min=3, max=256))
    ingredients = fields.List(
        fields.Str(required=True),
        required=True,
        validate=validate.Length(min=1)
    )
    instructions = fields.List(
        fields.Str(required=True),
        required=True,
        validate=validate.Length(min=1)
    )

# Instantiate the schemas for use in our routes
user_registration_schema = UserRegistrationSchema()
generate_recipe_schema = GenerateRecipeSchema()
save_recipe_schema = SaveRecipeSchema()
