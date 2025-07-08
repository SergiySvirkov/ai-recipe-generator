# Phase 2: Database Setup Guide
<!-- This document explains how to set up the database, initialize the schema, and populate it with initial data. -->

## 1. Overview

This project uses **Flask-SQLAlchemy** as an ORM (Object-Relational Mapper) to interact with the database and **Flask-Migrate** (which uses Alembic) to handle database schema migrations.

- **For development:** We use a simple file-based **SQLite** database (`dev.db`).
- **For production:** The architecture is designed to easily switch to **PostgreSQL**.

The database models are defined in `app/models.py`.

## 2. Setup and Initialization Steps

Follow these steps from the root directory of the project to set up your local database.

### Step 1: Install Dependencies

First, ensure you have all the necessary Python packages installed. Make sure your virtual environment is activated.

```bash
# Install Flask, SQLAlchemy, and tools for database interaction
pip install Flask Flask-SQLAlchemy Flask-Migrate

# Install the database driver (for SQLite, it's built-in)
# For PostgreSQL, you would run: pip install psycopg2-binary

Step 2: Initialize the Database Migrations

This command needs to be run only once. It creates a migrations directory, which will store all the database schema changes.

# Set the FLASK_APP environment variable
export FLASK_APP=manage.py  # On Windows use: set FLASK_APP=manage.py

# Initialize the migration repository
flask db init

Step 3: Create the First Migration

Flask-Migrate will inspect your models in app/models.py and generate a migration script that creates the corresponding tables.

# Generate the initial migration script
flask db migrate -m "Initial migration: Create user, recipe, and ingredient tables"

You will see a new file in the migrations/versions/ directory. This file contains the Python code to create your tables.
Step 4: Apply the Migration to the Database

This command executes the migration script, which will create the dev.db file (if it doesn't exist) and create all the tables inside it.

# Apply the migration to the database
flask db upgrade

After this step, you have an empty but correctly structured database.
Step 5: Seed the Database with Initial Data

The scripts/seed_database.py script populates the database with recipes from the data/train_dataset.json file.

# Run the seeding script
python scripts/seed_database.py

After this script finishes, your database will be populated with recipes, ingredients, and other initial data, ready for development.
Making Changes to the Schema

If you ever change the models in app/models.py (e.g., add a new column), you need to repeat steps 3 and 4 to update your database schema:

# 1. Generate a new migration script
flask db migrate -m "Description of your change"

# 2. Apply the new migration
flask db upgrade
