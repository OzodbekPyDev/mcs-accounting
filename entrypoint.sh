#!/bin/bash

# Function to wait for PostgreSQL to be ready
wait_for_postgres() {
    echo "Waiting for PostgreSQL to be ready..."

    # Loop until we can make a successful connection to PostgreSQL
    while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
        sleep 1
    done

    echo "PostgreSQL is ready."
}

# Run the wait function
wait_for_postgres

# Run Alembic migrations
alembic upgrade head

# Start the FastAPI application
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT