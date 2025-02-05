#!/bin/sh

echo "Waiting for PostgreSQL to start..."

while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL started!"

python manage.py migrate

python manage.py collectstatic --noinput

python seed_data.py

python manage.py runserver 0.0.0.0:8000
