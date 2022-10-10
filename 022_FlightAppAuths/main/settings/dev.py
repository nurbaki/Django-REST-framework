from .base import * 

# on Test:

DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# for debug:
INTERNAL_IPS = [ 
    "127.0.0.1", 
]

# LOGS:
LOGGING = { 
    "version": 1, 
    "disable_existing_loggers": True, 
    "formatters": { 
        "standard": { 
            "format": "[%(levelname)s] %(asctime)s %(name)s: %(message)s" 
        }, 
        'detail': { 
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}', 
            'style': '{', 
        },
    }, 
    "handlers": { 
        "console": { 
            "class": "logging.StreamHandler", 
            "formatter": "standard", 
            "level": "ERROR", 
            "stream": "ext://sys.stdout", 
            }, 
        'file': { 
            'class': 'logging.FileHandler', 
            "formatter": "detail", 
            'filename': './dev_logs.log', 
            'level': 'WARNING',
        }, 
    }, 
    "loggers": { 
        "django": { 
            "handlers": ["console", 'file'], 
            "level": config("DJANGO_LOG_LEVEL", "WARNING"), 
            'propagate': True, 
        }, 
    }, 
}

# SQLite:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'dev_db.sqlite3',
    }
}
