#!/bin/bash

echo "Generating Alembic migrations..."
alembic revision --autogenerate -m "betmodel"

echo "Applying Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI server..."
uvicorn main:app --reload --host 0.0.0.0
