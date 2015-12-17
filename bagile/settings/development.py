from bagile.settings.common import *

DEBUG = True

ALLOWED_HOSTS = []

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
]

STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'collected_media')
