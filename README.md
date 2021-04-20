# edagames-django

[![evbeda](https://circleci.com/gh/evbeda/edagames-client.svg?style=shield&circle-token=e93c0f1353243455610bd2f48cf8fb877626c4eb)](https://circleci.com/gh/evbeda/edagames-django)

[![Maintainability](https://api.codeclimate.com/v1/badges/40a2e96df1f2056ea2c4/maintainability)](https://codeclimate.com/github/evbeda/edagames-django/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/40a2e96df1f2056ea2c4/test_coverage)](https://codeclimate.com/github/evbeda/edagames-django/test_coverage)

## DOCKER
#### Requirements
First you need to install Docker for Mac in your computer by doing [click here](https://www.docker.com/products/docker-desktop).
> **NOTE:** Download `Mac with Intel Chip` option.

Also you need to create a `.env` file in your local repository to add all enviroment variables.
```
SECRET_KEY=************************************************
SECRET_KEY_JWT=************
SOCIAL_AUTH_FACEBOOK_KEY=******************
SOCIAL_AUTH_FACEBOOK_SECRET=*******************************
```

#### Execution
To run the docker container with docker-compose execute:
```
docker-compose up -d
```
> **NOTE:** You must be in /edagames-django folder.