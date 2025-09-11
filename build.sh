#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py createsuperuser --noinput

python manage.py migrate
