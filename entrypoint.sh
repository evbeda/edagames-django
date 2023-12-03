#!/bin/sh
# python manage.py migrate --settings=edagames.settings.prod
# python manage.py runserver 0.0.0.0:8000 --settings=edagames.settings.prod
python manage.py migrate --settings=edagames.settings.local
python manage.py runserver 0.0.0.0:8000 --settings=edagames.settings.local
