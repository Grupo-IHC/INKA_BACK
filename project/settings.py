"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from decouple import config, Csv
from datetime import timedelta
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r91d9ymj!9c#g9241btg**518b#2n*ji&&%c%&ja#4jlrh1y#s'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS', 'https://localhost')]
CSRF_TRUSTED_ORIGINS = ['https://inkaback-production.up.railway.app']

CORS_ORIGIN_WHITELIST = [
    'http://localhost:5173',
    'http://localhost:5173/',
    'http://inka-kappa.vercel.app',
    'http://inka-kappa.vercel.app/',
]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'storages',
    'corsheaders',
    
    'security',
    'product',
    'inventory',
    'sales',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE'   : 'django.db.backends.postgresql',
        'NAME'     : os.environ.get('DB_NAME'),
        'USER'     : os.environ.get('DB_USER'),
        'PASSWORD' : os.environ.get('DB_PASSWORD'),
        'HOST'     : os.environ.get('DB_HOST'),
        'PORT'     : os.environ.get('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

THOUSAND_SEPARATOR = ','
NUMBER_GROUPING = 3
DECIMAL_SEPARATOR = '.'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICSFILES_DIRNAME = 'staticfiles'
if not os.path.exists(os.path.join(BASE_DIR,  STATICSFILES_DIRNAME)):
    os.makedirs(os.path.join(BASE_DIR,  STATICSFILES_DIRNAME))

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, STATICSFILES_DIRNAME),
)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_DIRNAME = 'media'
if not os.path.exists(os.path.join(BASE_DIR,  MEDIA_DIRNAME)):
    os.makedirs(os.path.join(BASE_DIR,  MEDIA_DIRNAME))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),  # Cambia el tiempo de sesión del token de acceso según tus necesidades.
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=2),  # Cambia el tiempo de vida del token de actualización según tus necesidades.
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),  # Tiempo máximo de vida del token de actualización.
    'SLIDING_TOKEN_REFRESH_GRACE_PERIOD': timedelta(days=4),  # Período de gracia para actualizar el token antes de que expire.
    'ALGORITHM': 'HS256',  # Algoritmo de encriptación, puedes cambiarlo según tus necesidades.
    'SIGNING_KEY': SECRET_KEY,  # Clave secreta de tu aplicación.
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication', 
    ),
}

JWT_AUTH = {
    # how long the original token is valid for
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7 if DEBUG else 1),
    # 'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=60 if DEBUG else 1),

    # allow refreshing of tokens
    'JWT_ALLOW_REFRESH': True,

    # this is the maximum time AFTER the token was issued that
    # it can be refreshed.  exprired tokens can't be refreshed.
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_RESPONSE_PAYLOAD_HANDLER': 'aios.views.jwt_response_payload_handler'
}

CONTENT_TYPE = 'application/json; charset=utf-8'
FILE_UPLOAD_PERMISSIONS=0o644

CORS_ALLOWED_ORIGINS = [
    # Aquí puedes agregar los dominios permitidos para realizar solicitudes
    # Puedes utilizar '*' para permitir todos los dominios, pero esto no es recomendado en producción
    # 'http://example.com',
    # 'https://example.com',
    'http://localhost:8000',
    # 'http://localhost:5173',
    # '*'
]

CORS_ALLOW_ALL_ORIGINS = True  # Establece esto en True si deseas permitir todos los dominios

CORS_ALLOW_CREDENTIALS = True  # Establece esto en True si deseas permitir el envío de cookies en las solicitudes

CORS_ALLOWED_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SIGNATURE_NAME = os.environ.get('AWS_S3_SIGNATURE_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERIFY = True
# DEFAULT_FILE_STORAGE = config('AWS_DEFAULT')

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "WEB": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        "OPTIONS": {
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# STATICFILES_STORAGE = "storages.backends.s3.S3Storage"
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = 'sellosinkasac@gmail.com'
EMAIL_HOST_USER = 'sellosinkasac@gmail.com'
EMAIL_HOST_PASSWORD = 'caocmannsmfhahwa'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

PASSWORD_RESET_TIMEOUT = 14400

APPEND_SLASH = False