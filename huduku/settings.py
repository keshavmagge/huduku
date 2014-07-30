"""
For more information on django settings, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os

BASE_DIR    = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.normpath(os.path.join(BASE_DIR, os.pardir))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cps',
        'USER': 'cobrain',
        'PASSWORD': 'cobrain',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


DEBUG            = True
TEMPLATE_DEBUG   = True

ALLOWED_HOSTS    = []

INSTALLED_APPS   = (
    # Django Apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'tastypie',
    'grappelli',
    'django.contrib.admin', # Has to come after Grappelli
    'huduku',
)

ROOT_URLCONF = 'huduku.urls'

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'America/New_York'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True

STATIC_URL          =  '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS    = (
    os.path.join(PROJECT_DIR, 'static'),
)

TEMPLATE_DIRS       = (
    os.path.join(PROJECT_DIR, 'templates'),
)

MEDIA_URL           = "/media/"

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "social.apps.django_app.context_processors.backends",
    "social.apps.django_app.context_processors.login_redirect",
)

ADMINS = (
    ('Keshav Magge', 'keshav@cobrain.com'),
)

SECRET_KEY = '6d74#p*so6%i#^=r-2n44sqp)*n$lfyno=oxgqkk4p25al18b*'

SOLR = "http://localhost:8080/solr"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'verbose': {
            'format': '[%(levelname)s %(process)d:%(thread)d %(asctime)s %(module)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
