from pathlib import Path
import os
from base.crypto import secret_key

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-e!6*&iwd5z*29wl63m0*=-i^sna(!imx%22ytcpk05d1*8@mb#'
CRYPTO_KEY = secret_key



#DEBUG = int(os.environ.get("DEBUG", default=0))
DEBUG = True

ALLOWED_HOSTS = ['localhost', 'efs.com', '127.0.0.1','192.168.0.148']
#ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")


SESSION_EXPIRED_AT_BROWSER_CLOSE = True
SESSION_COOKIES_AGE = 1
SESSION_SAVE_EVERY_REQUEST = True

# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True


# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'base.apps.BaseConfig',
    'accounts',

    # pip install psycopg2

    'rest_framework',  # pip install djangorestframework
    'rest_framework.authtoken',

    #'elasticsearch_dsl',
    #'django_elasticsearch_dsl',             # pip install elasticsearch-dsl  and django-elasticsearch-dsl

    'cryptography',  # pip install django-cryptography ---------------this will install the following two packeges
    'django_cryptography',
]


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },

    {'NAME': 'storage.validators.UppercaseValidator', },
    {'NAME': 'storage.validators.LowercaseValidator', },
    {'NAME': 'storage.validators.SymbolValidator', },
]
# ELASTICSEARCH_DSL = {
#     'default': {
#         'hosts': os.environ.get("ELASTICSEARCH_DSL_HOSTS", 'localhost:9200')
#     },
# }


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '0/day',
        'user': '400/day',
    },

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
}



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'storage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'storage.wsgi.application'



# DATABASES = {
#     "default": {
#         "ENGINE": os.environ.get("SQL_ENGINE"),
#         "NAME": os.environ.get("SQL_DATABASE"),
#         "USER": os.environ.get("SQL_USER"),
#         "PASSWORD": os.environ.get("SQL_PASSWORD"),
#         "HOST": os.environ.get("SQL_HOST"),
#         "PORT": os.environ.get("SQL_PORT"),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# for nginx
# STATIC_ROOT = '/static/'
# STATIC_URL = '/static/'

# for 127.0.0.1:8000
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'



# for Nginx
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, '/media/')

# for 127.0.0.1:8000
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')