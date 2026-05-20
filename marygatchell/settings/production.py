import os
from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
ALLOWED_HOSTS = ['localhost','146.190.123.147', 'marygatchell.com','www.marygatchell.com' ]
cwd = os.getcwd()
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": f"{cwd}/.cache"
    }
}

# Enable per-site page caching (cache rendered pages for 10 minutes)
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = "marygatchell"
MIDDLEWARE = (
    ["django.middleware.cache.UpdateCacheMiddleware"]
    + MIDDLEWARE
    + ["django.middleware.cache.FetchFromCacheMiddleware"]
)


DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": os.environ.get('DB_NAME', 'marygatchell'),
        "USER": os.environ.get('DB_USER', 'marygatchell'),
        "PASSWORD": os.environ['DB_PASSWORD'],
        "HOST": os.environ.get('DB_HOST', 'localhost'),
        "PORT": os.environ.get('DB_PORT', '5432'),
    }
}


sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN', ''),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    _experiments={
        # Set continuous_profiling_auto_start to True
        # to automatically start the profiler on when
        # possible.
        "continuous_profiling_auto_start": True,
    },
)

try:
    from .local import *
except ImportError:
    pass
