from .base import *
import os


DEBUG = False
TEMPLATE_DEBUG = False

# static on prod
STATIC_URL = '//election_api.overcastcdn.com/'
COMPRESS_URL = STATIC_URL
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
STATICFILES_STORAGE = 'election_api.storage.CachedS3BotoStorage'
COMPRESS_STORAGE = 'election_api.storage.CachedS3BotoStorage'
DEFAULT_FILE_STORAGE = 'election_api.storage.CachedS3BotoStorage'


# redis cache on localhost
# remember to change database index
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        'OPTIONS': {
            # TODO change this
            'DB': 10,
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        }
    }
}

ALLOWED_HOSTS = [
    '*'
]

#Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES =  {
    'default': dj_database_url.config()
}

EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'app58346924@heroku.com'
EMAIL_HOST_PASSWORD = '1oy8v2v31303'

try:
    from .local import *
except ImportError:
    pass
