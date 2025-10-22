 # settings.py
from pathlib import Path
from datetime import timedelta
import os
import dj_database_url # <--- NEW: Import for Heroku Database

# -------------------------------------------------------------------------------------------------
# Environment Variables & Security
# -------------------------------------------------------------------------------------------------
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Use environment variables for production security (Heroku)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-b%uace_2_!av=je)abxqod*cs$f_eqlm3&&w3#x=v!o(**$27!')

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

# 🔴 FIX 1: Set the Custom User Model
# Replace 'YourCustomUser' with the exact name of your user model in users/models.py
AUTH_USER_MODEL = 'users.YourCustomUser'

# 🔴 FIX 2: Configure Database for Heroku (PostgreSQL)
# Default to SQLite for local development (if DATABASE_URL is not set)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Overwrite with Heroku's PostgreSQL config when DATABASE_URL environment variable is present
# This uses the dj_database_url package.
if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600, 
        ssl_require=True # Required for Heroku Postgres
    )

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

# Configure WhiteNoise Storage Backend for production serving.
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
        # If you want registration to be accessible to everyone, you'll need to 
        # set permission classes specifically on the register view to AllowAny.
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