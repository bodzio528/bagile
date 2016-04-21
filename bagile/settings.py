"""
Django settings for bagile project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import os

# production settings defined in secret.py
# which is not under version control
# -- create it by copying secret.py.template
import bagile.secret

BASE_DIR = bagile.secret.BASE_DIR
SECRET_KEY = bagile.secret.SECRET_KEY

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# Application definition

LOCAL_APPS = [
    'scrumboard',
]

THIRD_PARTY_APPS = [
    'bootstrap3',
    'colorfield',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bagile.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bagile.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
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

# DEVELOPMENT Databases
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# URL of the login page.
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/scrumboard/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files (uploaded Documents, users' Avatars)
MEDIA_URL = '/media/'

# Indicates if this is development or production
DEBUG = bagile.secret.DEBUG

CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG

if DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'collected_media')
else:
    DATABASES = bagile.secret.DATABASES
    STATIC_ROOT = bagile.secret.STATIC_ROOT
    MEDIA_ROOT = bagile.secret.MEDIA_ROOT

ALLOWED_HOSTS = bagile.secret.ALLOWED_HOSTS


BOOTSTRAP3 = {
    # The URL to the jQuery JavaScript file
    'jquery_url': 'https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js',

    # The Bootstrap base URL
    'base_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/',
}

GROUPS_PERMISSIONS = {
    'Developers': [
        'add_item',
        'change_item',
        'delete_item',
    ],
    'Scrum Masters': [
        'add_sprint',
        'change_sprint',
        'delete_sprint',
    ]
}
