# Phase 4: API Endpoints Guide
<!-- This document provides a detailed reference for all available API endpoints. -->

All endpoints are prefixed with `/api/v1`.

## 1. Authentication

### POST /users/register
Registers a new user.

- **Method:** `POST`
- **Body (JSON):**
  ```json
  {
    "username": "newuser",
    "password": "strongpassword123"
  }

    Success Response (201):

    {
      "message": "New user created!"
    }

    Error Responses: 400 (missing data), 409 (username exists).

POST /users/login

Logs in a user and returns a JWT for authentication.

    Method: POST

    Authentication: Basic Auth (Username and Password).

    Success Response (200):

    {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }

    Error Response: 401 (invalid credentials).

2. Recipe Generation
POST /generate-recipe

Generates a new recipe using the AI model. This endpoint is public and does not require authentication.

    Method: POST

    Body (JSON):

    {
      "ingredients": ["salmon", "lemon", "dill"],
      "diet": "any"
    }

    Success Response (200): A JSON object containing the generated recipe.

3. Saved Recipes (Protected)

These endpoints require a valid JWT to be sent in the x-access-token header.
POST /recipes

Saves a recipe for the authenticated user.

    Method: POST

    Headers: x-access-token: <your_jwt_token>

    Body (JSON):

    {
      "title": "AI Generated Salmon",
      "ingredients": ["1 lb salmon fillet", "1 lemon", "2 tbsp dill"],
      "instructions": ["Preheat oven...", "Place salmon on foil...", "Bake..."]
    }

    Success Response (201):

    {
      "message": "Recipe saved!",
      "id": 123
    }

GET /recipes

Retrieves all recipes saved by the authenticated user.

    Method: GET

    Headers: x-access-token: <your_jwt_token>

    Success Response (200):

    {
      "recipes": [
        {
          "id": 123,
          "title": "AI Generated Salmon",
          "ingredients": ["1 lb salmon fillet", "1 lemon", "2 tbsp dill"],
          "instructions": ["Preheat oven...", "Place salmon on foil...", "Bake..."]
        }
      ]
    }
