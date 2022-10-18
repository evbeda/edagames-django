# edagames-django

[![evbeda](https://circleci.com/gh/evbeda/edagames-client.svg?style=shield&circle-token=e93c0f1353243455610bd2f48cf8fb877626c4eb)](https://circleci.com/gh/evbeda/edagames-django)

[![Maintainability](https://api.codeclimate.com/v1/badges/40a2e96df1f2056ea2c4/maintainability)](https://codeclimate.com/github/evbeda/edagames-django/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/40a2e96df1f2056ea2c4/test_coverage)](https://codeclimate.com/github/evbeda/edagames-django/test_coverage)

## CLASS DIAGRAM
![alternative text](http://www.plantuml.com/plantuml/png/TP7FIWCn4CRlUOe5BthehL3eGKeBugMUz5ocoRIDJJAIJBo8x-wcSIVThIuip9_VzqqoMIM6oDaxbSusV404tsqSfFH4WJVaA7QGcJomrLFa6S5WN8C-7oFbO2f-Dv_Ff-GDSxXyLzWDiLWibD95tBqbZ5_AccLd0wlSPm4yBhl4KQ47wsfeW77tJZPWJvP4sRG3pVQpP_T4hkI9uN3uJR-70MlYvj-ycSuOQbY6xWP2T5jWVTgYtsDCpI1fYbZ3FR6eV84bkvwTDYTm3iCHZRYCf7hetyf5EbQAefsQAL_s5lYVYpI7OuyLIDPQe-OmDEzVAE13ytaLuezz5gmyPJURFPPhg_ulyMYDKXplHSfIKcDWqhosR3Dg-PAtaofHJHih32PxzmC0)

## DOCKER
### Requirements
First you need to install Docker for Mac in your computer by doing [click here](https://www.docker.com/products/docker-desktop).
> **NOTE:** Download `Mac with Intel Chip` option.

### First steps
Everytime you make migrations or modify the requirements.txt file you need to re-build the docker image.
To build the docker image run this command.
```
docker build . -t edagames-web
```
> docker build: build an image
> .: select all files
> -t: add a tag
> edagames-web: tag_name

Also you need to create an `.env` file in your local repository to add all enviroment variables.
```
SECRET_KEY=************************************************
SECRET_KEY_JWT=************
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY=******************
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET=*******************************
SERVER_URL=http://127.0.0.1
SERVER_PORT=5000
```

### Execution
To run the docker container with docker-compose execute:
```
docker-compose up -d
```
> **NOTE:** You must be in /edagames-django folder.

### End Docker process
To kill a docker-compose process you must run this command:
```
docker-compose down
```

### Run docker-compose for Web and Server
Create a folder edagames which contains all repos.
Then add this file as a `.yml`
```
version: "3.9"
services:
    server:
        build: 
            context: ./edagames-server
        ports:
            - "5000:5000"
        environment: 
            - TOKEN_KEY

    edagames-web:
        build: 
            context: ./edagames-django
        ports:
            - "8000:8000"
        volumes: 
            - .:/edagames-django
        environment: 
            - SECRET_KEY=${SECRET_KEY}
            - SECRET_KEY_JWT=${SECRET_KEY_JWT}
            - SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY=${SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY}
            - SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET=${SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET}
            - SERVER_URL=server
            - SERVER_PORT=5000

    edagames-quoridor:
        build:
            context: ./edagames-quoridor
        ports:
            - "50051:50051"

```
### How to run the test
in the same pwd as the manage.py run
```
python3 manage.py test
```
if you want to see the coverage and generate a html coverage
```
coverage run manage.py test && pipenv run coverage xml && pipenv run coverage report -m
```

### Problems that you could have
1 - If you are having problems installing mysql-client go and follow the steps on https://pypi.org/project/mysqlclient/