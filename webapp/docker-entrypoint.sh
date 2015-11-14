#!/bin/bash
set -e
# Should really have a test here to make sure DB is up.
echo "Waiting for DB to be set up"
sleep 10
echo "Migrating and starting server"
python manage.py makemigrations
python manage.py migrate
python -u manage.py runserver 0.0.0.0:8000