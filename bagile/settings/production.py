from bagile.settings.common import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

STATIC_ROOT = '/srv/http/bagile/static'
MEDIA_ROOT = '/srv/http/bagile/media'
