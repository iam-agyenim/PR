import os
from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False
SECRET_KEY = 'Kobbyhbjj^-f71+0l2+0=75y1iza&4@_+l3bu+_srpzu4$d3k'  
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '146.190.123.147']
cwd = os.getcwd()
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": f"{cwd}/.cache"
    }
}


DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": 'marygatchell',
        "USER": 'marygatchell',
        "PASSWORD": 'Kobbypraize1234@#$',
        "HOST": 'localhost',
        "PORT": "5432",
    }
}



sentry_sdk.init(
    dsn="https://fed26037191263aef5c36b01809472ac@o4508445830021120.ingest.us.sentry.io/4508445834149888",
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
