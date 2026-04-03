#!/bin/sh

echo "Running database migrations..."
alembic upgrade head

echo "Checking if database needs seeding..."
ROW_COUNT=$(python -c "from database import SessionLocal; db=SessionLocal(); print(db.execute('SELECT COUNT(*) FROM customers').scalar())" 2>/dev/null || echo "0")

if [ "$ROW_COUNT" -eq 0 ]; then
    echo "Database is empty. Seeding initial data..."
    python seed.py
else
    echo "Database already has data. Skipping seed."
fi

echo "Starting FastAPI application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000