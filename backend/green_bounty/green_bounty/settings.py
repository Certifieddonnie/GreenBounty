"""
Django settings for green_bounty project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
import datetime
from dotenv import load_dotenv

# settings.py

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json


load_dotenv()
# Option 1: Load from a file path (for development, ensure it's outside version control)
# FIREBASE_SERVICE_ACCOUNT_PATH = os.path.join(BASE_DIR, 'path/to/your/serviceAccountKey.json')
# cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_PATH)

# Option 2: Load from an environment variable (recommended for production)
# The JSON content should be base64 encoded or stored directly as a string
# For example, if you store the entire JSON as an environment variable:
# FIREBASE_SERVICE_ACCOUNT_JSON = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON')
# if FIREBASE_SERVICE_ACCOUNT_JSON:
#     service_account_info = json.loads(FIREBASE_SERVICE_ACCOUNT_JSON)
#     cred = credentials.Certificate(service_account_info)
# else:
#     # Handle the case where the environment variable is not set (e.g., error or default to file)
#     raise Exception("FIREBASE_SERVICE_ACCOUNT_JSON environment variable not set.")


# For simplicity in this example, let's assume you're loading from a file path
# during development. IMPORTANT: CHANGE THIS FOR PRODUCTION!
FIREBASE_SERVICE_ACCOUNT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.environ.get('SERVICE_ACCOUNT_KEY_PATH'))

# Replace 'your-firebase-project-service-account-key.json' with the actual filename
# and ensure it's in a secure location (e.g., outside your project directory,
# or ensure it's not committed to git).

if os.path.exists(FIREBASE_SERVICE_ACCOUNT_PATH):
    cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': os.environ.get('FIREBASE_REALTIME_DATABASE_URL')
    })
else:
    print(f"WARNING: Firebase service account key not found at {FIREBASE_SERVICE_ACCOUNT_PATH}. "
          "Firebase Realtime Database operations will not work.")
    # You might want to raise an exception or handle this more robustly in production.


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-Party Apps
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_jwt',
    'treblle',

    # Local Apps
    'users',
    'fruits',
    'wallet',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'treblle.middleware.TreblleMiddleware',
]

ROOT_URLCONF = 'green_bounty.urls'

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

WSGI_APPLICATION = 'green_bounty.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, "green_bounty", "my.cnf")
        },
    }
}


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ]
}

# JWT Authentication COnfig
JWT_AUTH = {
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=3),
}


# Treblle Configuration Code
TREBLLE_HIDDEN_KEYS = ["id", "email", "password"]


TREBLLE_INFO = {
    'api_key': os.environ.get('TREBLLE_API_KEY'),
    'project_id': os.environ.get('TREBLLE_PROJECT_ID'),
    'hidden_keys': TREBLLE_HIDDEN_KEYS
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

# User Model
AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

APPEND_SLASH = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
