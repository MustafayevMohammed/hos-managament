#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input
# gunicorn core.wsgi:application --workers 4 --bind 0.0.0.0:8000

gunicorn core.wsgi:application --bind 0.0.0.0:$PORT