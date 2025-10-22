# settings.py
from pathlib import Path
from datetime import timedelta
import os

# -------------------------------------------------------------------------------------------------
# Environment Variables & Security
# -------------------------------------------------------------------------------------------------
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Use environment variables for production security (Heroku)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-b%uace_2_!av=je)abxqod*cs$f_eqlm3&&w3#x=v!o(**$27!')

# 💡 CHANGE 1: Set DEBUG safely for production.
# This checks for an environment variable called DJANGO_DEBUG.
# If not present (like on Heroku by default), DEBUG will be False.
DEBUG = os.environ.get('DJANGO_DEBUG') == 'True' 

# ALLOWED_HOSTS for Heroku
ALLOWED_HOSTS = ['caleb-task-manager-api-c26733b39359.herokuapp.com', '127.0.0.1', 'localhost']

# -------------------------------------------------------------------------------------------------
# Application definition
# -------------------------------------------------------------------------------------------------
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    # Local apps
    'tasks',
    "users",
]

# -------------------------------------------------------------------------------------------------
# Middleware
# -------------------------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise must be right after SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# -------------------------------------------------------------------------------------------------
# Database, Auth, and Internationalization
# -------------------------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------------------------------------------------------------------------
# Static files (CSS, JavaScript, Images)
# -------------------------------------------------------------------------------------------------
STATIC_URL = '/static/'
# Directory where collectstatic puts all files for production
STATIC_ROOT = BASE_DIR / 'staticfiles' 

# Extra directories Django should look in for static files (in addition to 'static/' inside apps)
STATICFILES_DIRS = [
    BASE_DIR / "static",
    # include the templates/static folder where the project currently stores CSS
    BASE_DIR / "core" / "templates" / "static",
]

# 💡 CRITICAL CHANGE 2: Configure WhiteNoise Storage Backend.
# This tells Django to use WhiteNoise's storage backend, which handles compression 
# and manifest creation for production serving and efficient caching.
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# -------------------------------------------------------------------------------------------------
# Django REST Framework & JWT setup
# -------------------------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',     # JWT auth
        'rest_framework.authentication.SessionAuthentication',          # Browsable API
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', # Require login by default
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}