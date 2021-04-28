# edagames-django

[![evbeda](https://circleci.com/gh/evbeda/edagames-client.svg?style=shield&circle-token=e93c0f1353243455610bd2f48cf8fb877626c4eb)](https://circleci.com/gh/evbeda/edagames-django)

[![Maintainability](https://api.codeclimate.com/v1/badges/40a2e96df1f2056ea2c4/maintainability)](https://codeclimate.com/github/evbeda/edagames-django/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/40a2e96df1f2056ea2c4/test_coverage)](https://codeclimate.com/github/evbeda/edagames-django/test_coverage)

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
SOCIAL_AUTH_FACEBOOK_KEY=******************
SOCIAL_AUTH_FACEBOOK_SECRET=*******************************
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
            - SOCIAL_AUTH_FACEBOOK_KEY=${SOCIAL_AUTH_FACEBOOK_KEY}
            - SOCIAL_AUTH_FACEBOOK_SECRET=${SOCIAL_AUTH_FACEBOOK_SECRET}
            - SERVER_URL=server
            - SERVER_PORT=5000
```
