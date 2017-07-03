"""
Django settings for inferno project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Domain name
DOMAIN = 'campass.com.tw'
USERPOOL_URL = 'http://login.campass.com.tw'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open(BASE_DIR + '/config/' + 'secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ['.' + DOMAIN, 'localhost', '127.0.0.1', '0.0.0.0']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + [
    'djangobower',
    'webpack_loader',
    'infernoWeb',
    'slothTw',
    'arrogant',
    'greed'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inferno.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'inferno.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

from .settings_database import DATABASE_SETTINGS
if DEBUG:
    DATABASES = DATABASE_SETTINGS['sqlite']
else:
    DATABASES = DATABASE_SETTINGS['mysql']


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Shared session

SESSION_COOKIE_DOMAIN = '.' + DOMAIN
with open(BASE_DIR + '/config/' + 'sessionid.txt') as f:
    SESSION_COOKIE_NAME = f.read().strip()

# CORS header

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_REGEX_WHITELIST = (
    '^(https?://)www.' + DOMAIN,
    '^(https?://)localhost$',
    '(https?://)127.0.0.1'
)
CORS_ALLOW_METHODS = (
    'GET',
)

# django-bower allow django use bower to manage front-end library.

BOWER_COMPONENTS_ROOT = BASE_DIR
STATICFILES_DIRS.append(BOWER_COMPONENTS_ROOT)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)


BOWER_INSTALLED_APPS = (
    'd3#3.5.17',
    'radar-chart-d3',
    'jquery#2.2.4',
    'semantic#2.2.10',
    'toastr#2.1.3'
)

# Dev

if DEBUG:
    USERPOOL_URL = 'http://test.localhost.login.campass.com.tw:8080'
    CORS_ORIGIN_ALLOW_ALL = True
    del SESSION_COOKIE_DOMAIN


# react js config, using webpack
STATICFILES_DIRS = (
    #This lets Django's collectstatic store our bundles
    os.path.join(BASE_DIR, 'assets'), 
)

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}