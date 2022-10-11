"""
Django settings for edagames project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import os
from environment import load_env_var
from django.contrib.messages import constants as message_constants
import boto3
import base64
from botocore.exceptions import ClientError

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = load_env_var('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'edagames',
    'auth_app',
    'development',
    'tournaments',
    'social_django',
    'bootstrap4',
    'rest_framework',
    'django_tables2',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'edagames.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.linkedin.LinkedinOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

WSGI_APPLICATION = 'edagames.wsgi.application'


# get secret
def get_secret(db_secret_name):

    secret_name = db_secret_name
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
   
    secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    return secret_value_response


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
secret_value = get_secret(load_env_var('DB_SECRET_NAME'))

DATABASES = {
    'default': {
        'ENGINE': secret_value["engine"],
        'NAME': secret_value["dbClusterIdentifier"],
        'USER': secret_value["username"],
        'PASSWORD': secret_value["password"],
        'HOST': secret_value["host"],
        'PORT': secret_value["port"]
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = "auth_app.User"

# Social Auth Pipeline
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'auth_app.pipeline.create_bot',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login'
STATICFILES_DIRS = ['static']
CRISPY_TEMPLATE_PACK = 'bootstrap4'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = load_env_var('SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY')
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = load_env_var('SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET')
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_emailaddress', 'r_liteprofile']
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ['emailAddress', 'formatted-name']
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [
    ('formatted-name', 'username'),
    ('emailAddress', 'email_address'),
]

# Message TAG
MESSAGE_TAGS = {message_constants.ERROR: 'danger'}

# Server
SERVER_URL = load_env_var('SERVER_URL')
SERVER_PORT = load_env_var('SERVER_PORT')
