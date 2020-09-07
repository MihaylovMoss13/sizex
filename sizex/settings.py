import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '_)zw9%okw9un+9g0@6)s@d8hi(om**7rt3z6j*up5js$d77f3n'

from sizex.custom_settings import *

# CACHE
PROJECT_APPS = [
    'pages',
]

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mptt',
    'django_mptt_admin',
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',
    'compressor',
    'adminsortable2',
    # 'cacheops',
] + PROJECT_APPS

MIDDLEWARE = [
    'pages.middleware.RedirectMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'pages.middleware.MobileMiddleware',
    'pages.middleware.VaryMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sizex.urls'

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
                'django.template.context_processors.i18n',
                'sizex.context_processors.app',
            ],
        },
    },
]

WSGI_APPLICATION = 'sizex.wsgi.application'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

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

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'bootstrapck',
        'allowedContent': True,
        'toolbar': 'full',
    },
    'inline': {
        'skin': 'bootstrapck',
        'allowedContent': True,
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['Image'],
            ['RemoveFormat', 'Source']
        ],
        'height': 100,
        'width': 400
    }
}

CONTACTS = {
    'PHONE': ('+74957233013', '+7 (495) 723-30-13'),
    'MOBILE': ('+79859232316', '+7 (985) 923-23-16'),
    'EMAIL': 'info@room-potolok.ru',
}

USER_AGENTS_DICT = {
    '(.*?)Android.*Mobile': 'android',
    '(.*?)Mobile.*Android': 'android',
    '(.*?)iPhone': 'iphone',
    '(.*?)BlackBerry': 'blackberry',
    '(.*?)Symbian': 'symbian',
    '(.*?)Windows Phone': 'win',
    '(.*?)Windows CE': 'win',
    '(.*?)Windows Mobile': 'win',
    '(.*?)Opera Mini': 'opera',
    '(.*?)Opera Mobi': 'opera',
}

USER_AGENTS = re.compile('|'.join(USER_AGENTS_DICT.keys()))

RESOLUTION_KEY = 'resolution'

EXCLUDE_FROM_MINIFYING = ('myadmin/', 'ckeditor/', 'jet/')

# CACHEOPS = {
#     'pages.*': {'ops': ('all'), 'timeout': 60 * 60 * 12},
# }

# if DEBUG:
#     INSTALLED_APPS += ('debug_toolbar',)
#     MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
