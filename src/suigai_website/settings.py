import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

BOOTSTRAP5_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "..", "django_bootstrap5"))
if BOOTSTRAP5_FOLDER not in sys.path:
    sys.path.insert(0, BOOTSTRAP5_FOLDER)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gut+seym7@^5p8p_pb+0qj9&r7r%j*2r#gr%e+!85e6bq2fm$c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

### Application definition
### Activating models
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ### Common Applications
    'P0000Dummy.apps.P0000DummyConfig',
    'P0100Login.apps.P0100LoginConfig',
    ### Excel Applications
    'P0200ExcelDownload.apps.P0200ExcelDownloadConfig',
    'P0300ExcelUpload.apps.P0300ExcelUploadConfig',
    ### Online Applications
    'P0400OnlineDisplay.apps.P0400OnlineDisplayConfig',
    'P0500OnlineUpdate.apps.P0500OnlineUpdateConfig',
    ### Area Applications
    'P0600AreaCreate.apps.P0600AreaCreateConfig',
    ### Admin Applications
    'P9100AdminCheck.apps.P9100AdminCheckConfig',
    'P9200AdminHistory.apps.P9200AdminHistoryConfig',
    'P9300AdminLock.apps.P9300AdminLockConfig',
    
    'django.contrib.sites',
    ### See https://office54.net/python/django/django-bootstratp5-css
    'django_bootstrap5',
    'file_upload', ### 2022/04/22 Add
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

ROOT_URLCONF = 'suigai_website.urls'

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

WSGI_APPLICATION = 'suigai_website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        }
    },
    "loggers": {"django.request": {"handlers": ["mail_admins"], "level": "ERROR", "propagate": True}},
}

# Settings for django-bootstrap5
BOOTSTRAP5 = {
    "error_css_class": "django_bootstrap5-error",
    "required_css_class": "django_bootstrap5-required",
    "javascript_in_head": True,
}