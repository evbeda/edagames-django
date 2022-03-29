FROM python:3.8-slim

WORKDIR /edagames-django

RUN apt-get update && apt-get install -y python3-dev default-libmysqlclient-dev build-essential

COPY requirements.txt /edagames-django
RUN pip install -r requirements.txt

COPY . /edagames-django

EXPOSE 8000

ENTRYPOINT [ "./entrypoint.sh" ]
