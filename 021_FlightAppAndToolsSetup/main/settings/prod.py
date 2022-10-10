from .base import *

# on Live:

DEBUG = False
ALLOWED_HOSTS = [
    '127.0.0.1',
]



# SQLite:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_live.sqlite3',
    }
}


# # PostreSQL:
# DATABASES = { 
#     "default": { 
#         "ENGINE": "django.db.backends.postgresql_psycopg2", 
#         "NAME": config("POSTRESQL_DATABASE"), 
#         "USER": config("POSTRESQL_USER"), 
#         "PASSWORD": config("POSTRESQL_PASSWORD"), 
#         "HOST": config("POSTRESQL_HOST"), 
#         "PORT": config("POSTRESQL_PORT"), 
#         "ATOMIC_REQUESTS": True, 
#     }
# }