#!/bin/sh

echo "Waiting for PostgreSQL to start..."
while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL started!"

# Run Django migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Seed initial data
python seed_data.py

# Start the Django development server
python manage.py runserver 0.0.0.0:8000
