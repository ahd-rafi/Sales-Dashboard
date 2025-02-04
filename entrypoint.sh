#!/bin/sh

echo "Waiting for PostgreSQL to start..."
# Wait for PostgreSQL to be ready
while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL started!"

# Run Django migrations and collect static files
python manage.py migrate
python manage.py collectstatic --noinput

# Run the Django development server
python manage.py runserver 0.0.0.0:8000
