"""
Django settings for iotlimsintegrator project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4w*2%x$31l-6h+umsq&$7&v!3x1uswe==39bmrdm3l5l%&x4$s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'admin_tools_stats',
    'dashboard',
    'django_nvd3',
    'rangefilter',
    'csp',
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'userauthentication',
    'core',
    'auditlog',
    'audit',
    'apidetails',
    'eventmanagement',
    'masterdata',
    'django_celery_results',
    'django_celery_beat',
    'task',
    'import_export',
    'refenrencetype',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
]

ROOT_URLCONF = 'iotlimsintegrator.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_auto_logout.context_processors.auto_logout_client',
            ],
        },
    },
]

WSGI_APPLICATION = 'iotlimsintegrator.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'iotlimsintegrator',
        'USER': 'postgres',
        'PASSWORD': 'Mnop@1234',
        'HOST': 'localhost'
    }
}

# Cache Configuration
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

CACHE_TIMEOUT = 300  # 5 minutes

# Use cache-backed sessions
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
# Set session cookie age to 15 minutes (15 minutes * 60 seconds)
SESSION_COOKIE_AGE = 900
SESSION_CUSTOM_COOKIE_AGE = 300
SESSION_SAVE_EVERY_REQUEST = True

# Logger Configuration
# settings.py

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/info/info.log'),
            'maxBytes': 1024 * 1024 * 300,  # 300 MB
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8'
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/error/error.log'),
            'maxBytes': 1024 * 1024 * 300,  # 300 MB
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'info'],
            'level': 'INFO',
            'propagate': True,
        },
        'error_log': {
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URLS = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    'site_title': "Nexus Fusion",
    'site_header': 'Nexus Fusion',
    'site_brand': ' ',
    'site_logo': 'assets/imgs/Nexus Fusion.png',
    'copyright': 'EPAM.COM',
    "site_logo_classes": "custom-image",
    "custom_css": "css/app.css",

    'welcome_sign': 'Nexus Fusion Login',
    'order_with_respect_to': ["core", "core.iot_type",
                              "core.iot_device", "masterdata", "masterdata.unit", "masterdata.param",
                              "masterdata.event_type", "masterdata.event_type_iot_type_map",
                              "apidetails", "apidetails.applicationdetail", "apidetails.apidetail", "eventmanagement",
                              "eventmanagement.event_rule", "task", "task.customperiodictask", "dashboard",
                              "refenrencetype", "auth", "userauthentication", "auditlog", "audit"],
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"app": "core"}, {"app": "masterdata"}, {"app": "refenrencetype"}, {"app": "apidetails"},
        {"app": "eventmanagement"}, {"app": "task"}, {"app": "dashboard"},
    ],
    "show_sidebar": True,
    # "show_ui_builder": True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-light",
    "accent": "accent-primary",
    "navbar": "navbar-secondary navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "sandstone",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": False
}

AUTH_USER_MODEL = 'userauthentication.User'

# DJANGO AUTO LOGOUT
AUTO_LOGOUT = {
    'IDLE_TIME': timedelta(minutes=15),
    'MESSAGE': 'The session has expired. Please login again to continue.',
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
}

# Celery Configuration Options
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

CELERY_RESULT_BACKEND = 'django-db'

# Celery Beat Configuration
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_APP_NAME = 'iotlimsintegrator'
CELERY_NAMESPACE = 'CELERY'
CELERY_LOG_FILE_FOR_INFO = 'log/info/task_log/info.log'
CELERY_LOG_FILE_FOR_ERROR = 'log/error/task_log/error.log'
CELERY_LOG_MAX_BYTES = 1024 * 1024 * 300
CELERY_LOG_BACKUP_COUNT = 10

# App Specific Properties
APPLICATION_TASK_HANDLER = 'task.tasks.task_handler'
APPLICATION_TASK_HANDLER_PROCESS_FOR_EM = 'evaluate_event_rule_condition'
APPLICATION_TASK_HANDLER_PROCESS_FOR_LIMS = 'execute_lims_api_data_processor'
APPLICATION_TASK_HANDLER_PROCESS_FOR_LIMS_CONNECTION = 'execute_lims_get_connection_api'
APPLICATION_IOT_DEVICE_APP_NAME = 'Elemental Machine'
APPLICATION_GET_ALL_IOT_DEVICE_INFO_API = 'api/machines.json'
APPLICATION_INDIVIDUAL_IOT_DEVICE_INFO_API = 'api/machines/[device.uuid].json'
APPLICATION_IOT_DEVICE_INFO_API_TOKEN_PROPERTY = 'access_token'
APPLICATION_IOT_DEVICE_INFO_API_TOKEN_ID = 'cdd3c8788c499ceb4fa508359a3df1cf3fa736bddaf0050590fd4c7c7186ad9f'
APPLICATION_LIMS_API_TOKEN_ID = ''
APPLICATION_APPNAMESFORDASHBOARD_REF_NO = '1'

IMPORT_EXPORT_SKIP_ADMIN_ACTION_EXPORT_UI = True
