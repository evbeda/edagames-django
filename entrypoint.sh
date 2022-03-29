#!/bin/sh
python manage.py migrate --settings=settings.prod
python manage.py runserver 0.0.0.0:8000 --settings=settings.prod
