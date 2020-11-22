#!/bin/sh

python manage.py collectstatic --no-input --clear
python manage.py makemigrations --noinput
python manage.py migrate --noinput
exec "$@"
