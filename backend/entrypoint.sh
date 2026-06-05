#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "collecting static files"
yes yes | python manage.py collectstatic

# Start server
echo "Starting server"
exec "${@}"
