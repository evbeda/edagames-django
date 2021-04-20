FROM python:3.8-slim

WORKDIR /edagames-django

COPY requirements.txt /edagames-django
RUN pip install -r requirements.txt

COPY . /edagames-django

EXPOSE 8000

CMD [ \
    "python manage.py migrate", \
    "python manage.py runserver 0.0.0.0:8000" \
]
