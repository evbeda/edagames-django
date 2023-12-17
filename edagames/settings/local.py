from .dev import *  # noqa
from environment import get_env_variable

SOCIAL_AUTH_REDIRECT_IS_HTTPS = False

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': get_env_variable('DJANGO_DB_NAME'),
#         'USER': get_env_variable('DJANGO_DB_USER'),
#         'PASSWORD': get_env_variable('DJANGO_DB_PASSWORD'),
#         'HOST': get_env_variable('DJANGO_DB_HOST'),
#         'PORT': get_env_variable('DJANGO_DB_PORT'),
#     }
# }

import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default=get_env_variable('DATABASE_URL'))
}
