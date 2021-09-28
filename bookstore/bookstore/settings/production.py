from .base import *  # Import base settings from settings/__init__.py

from decouple import config
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG_PRO')

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-gx%xf5_w)ldyq$_%a@-@xj9=7!+ep0@f$+^sa*bc)2x%6&=9=*'
SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = config('ALLOWED_HOSTS_PRD').split(' ')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE'),
        'USER': config('USERNAME_DB'),
        'PASSWORD': config('PASSWORD_DB'),
        'HOST': config('HOST'),
        'PORT': config('PORT'),
    }  
}

print(Path(BASE_DIR,'logs/bookstore.log'))

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {"level": "WARNING", "handlers": ["file"]},
    "handlers": {
          "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": Path(BASE_DIR,'logs/bookstore.log'),
            "formatter": "app",
        },
        "access_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": Path(BASE_DIR,'logs/gunicorn.access.log'),
            "formatter": "app",
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": Path(BASE_DIR,'logs/gunicorn.error.log'),
            "formatter": "app",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True
        },
        'gunicorn.error': {
            'level': 'ERROR',
            'handlers': ['error_file'],
            'propagate': True,
        },
        'gunicorn.access': {
            'level': 'INFO',
            'handlers': ['access_file'],
            'propagate': False,
        },
    },
    "formatters": {
        "app": {
            "format": (
                u"%(asctime)s [%(levelname)-8s] "
                "(%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
}




