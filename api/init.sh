#!/bin/bash

# Generate Alembic migrations
echo "Generating Alembic migrations..."
alembic revision --autogenerate -m "init"

# Apply migrations to the database
echo "Applying Alembic migrations..."
alembic upgrade head

# Launch FastAPI server
echo "Starting FastAPI server..."
uvicorn app:app --reload --host 0.0.0.0
