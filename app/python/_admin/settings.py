"""
Django settings for _admin project.

Generated by 'django-admin startproject' using Django 2.1.8.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys
import logging
logging.basicConfig(level=logging.DEBUG)

import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.info('BASE_DIR: %s'%BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1$6vig-^1ytye$9svhy**p=x^v$(7=!+fm749q0fy$rw#v7!0z'

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default' : dj_database_url.config(conn_max_age=500) # Parse database configuration from $DATABASE_URL
}
logging.info('DATABASE: %s'%DATABASES['default']['NAME'])

# SECURITY WARNING: don't run with debug turned on in production!
if DATABASES['default']['HOST'].find('localhost') == -1: # Running on another server
    DEBUG = False
    ENV = 'prod'
else: # Running on localhost
    DEBUG = True
    ENV = 'dev'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'demo',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

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

WSGI_APPLICATION = '_admin.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


if ENV == 'prod':
    SECURE_SSL_REDIRECT = True # [1]
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
if ENV == 'prod':
    ALLOWED_HOSTS = [] # Add prod URL's here
else:
    ALLOWED_HOSTS = ['*']
logging.info('ALLOWED_HOSTS: %s'%','.join(ALLOWED_HOSTS))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

import mimetypes
mimetypes.add_type("image/svg+xml", ".svg", True)

STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(os.path.abspath(os.path.join(BASE_DIR, os.pardir)), 'static') # Where the files are copied from...
]
logging.info('STATICFILES_DIRS: %s'%str(STATICFILES_DIRS)) # Inputs

# heroku config:set DISABLE_COLLECTSTATIC=1
STATIC_ROOT = os.path.join(os.path.abspath(os.path.join(BASE_DIR, os.pardir)), 'staticroot') # Where the files are copied to and served from...
logging.info('STATIC_ROOT: %s'%str(STATIC_ROOT))
STATIC_URL = '/static/'
logging.info('STATIC_URL: %s'%str(STATIC_URL))

#TEST_RUNNER = 'django.test.runner.DiscoverRunner'
TEST_RUNNER = 'demo.tests.DiscoverRunnerForPLUS' # This allows us to run tests in development without creating some hair-brained test db!

