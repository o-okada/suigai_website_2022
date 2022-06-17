import os
import sys
from pathlib import Path

### See django.pdf P442 Using a custom user model when starting a project
### from .models import USER

### Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

BOOTSTRAP5_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "..", "django_bootstrap5"))
if BOOTSTRAP5_FOLDER not in sys.path:
    sys.path.insert(0, BOOTSTRAP5_FOLDER)

### Quick-start development settings - unsuitable for production
### See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

### SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gut+seym7@^5p8p_pb+0qj9&r7r%j*2r#gr%e+!85e6bq2fm$c'

### SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

### Application definition
### Activating models

### See django.pdf P454.
### Authentication support is bundled as Django contrib module in django.contrib.auth.
### By default, the required configuration is already included in the settings.py
### generated by django-admin startproject, these consist of two items listed in
### your INSTALLED_APPS settings:
### 1. 'django.contrib.auth' contains the core of the authentication framework, and its default models.
### 2. 'django.contrib.contenttypes' is the Django content type system, which allows permissions to be 
### associated with models you create.
INSTALLED_APPS = [
    'django_bootstrap5',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    ### Common Applications
    'P0000Common.apps.P0000CommonConfig',
    'P0000Dummy.apps.P0000DummyConfig',
    'P0100Login.apps.P0100LoginConfig',
    
    ### Excel Applications
    'P0200ExcelDownload.apps.P0200ExcelDownloadConfig',
    'P0300ExcelUpload.apps.P0300ExcelUploadConfig',
    
    ### Online Applications
    'P0400OnlineDisplay.apps.P0400OnlineDisplayConfig',
    'P0500OnlineUpdate.apps.P0500OnlineUpdateConfig',
    
    ### Area Applications
    'P0600CreateArea.apps.P0600CreateAreaConfig',

    ### Report Applications

    ### Reverse Verification Applications
    'P0800Reverse.apps.P0800ReverseConfig',
    
    ### CI Applications
    'P0900CI.apps.P0900CIConfig',
    
    ### Admin Applications
    'P9100Transact.apps.P9100TransactConfig',
    'P9200Lock.apps.P9200LockConfig',
    
    ### See Python Django開発入門, P224
    ### 'allauth',
    ### 'allauth.account',
    ### 'accounts.apps.AccountsConfig',
    
    ### See vector-ium.com/django-mathfilters/
    ### 'mathfilters', 
]

### These items in your MIDDLEWARE setting:
### 1. SessionMiddleware manages sessions across request.
### 2. AuthenticationMiddleware associates users with requests using sessions.
### With these settings in place, running the command manage.py migrate
### creates the necessary database tables for auth related models and
### permissions for any models defined in your installed apps.
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

### Database
### https://docs.djangoproject.com/en/4.0/ref/settings/#databases
### DATABASES = {
###     'default': {
###         'ENGINE': 'django.db.backends.sqlite3',
###         'NAME': BASE_DIR / 'db.sqlite3',
###     }
### }
### DATABASES = {
###     'default': {
###         'ENGINE': 'django.db.backends.postgresql_psycopg2',
###         'NAME': 'postgres',
###         'USER': 'postgres',
###         'PASSWORD': 'postgres',
###         'HOST': '127.0.0.1',
###         'PORT': '5432',
###     }
### }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'suigai_web',
        'USER': 'frics',
        'PASSWORD': 'frics',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

### Password validation
### https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
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

### Internationalization
### https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

### Static files (CSS, JavaScript, Images)
### https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

### Default primary key field type
### https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
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

### Settings for django-bootstrap5
BOOTSTRAP5 = {
    "error_css_class": "django_bootstrap5-error",
    "required_css_class": "django_bootstrap5-required",
    "javascript_in_head": True,
}

### AUTH_USER_MODEL = 'P0100Login.MyUser'
### See Python Django開発入門, P224
### django-allauthで利用するdjango.contrib.sitesを使うためにサイト識別用IDを設定する。
SITE_ID=1

### See Python Django開発入門, P224
### 認証バックエンド（認証を検証するクラス）を２つ設定する。
### Djangoは認証バックエンドを複数設定できる。
### 具体的には、AUTHENTICATION_BACKENDSリストに設定した認証バックエンドを順に認証できるまで試行する。
### AUTHENTICATION_BACKENDS = (
###     ### 一般ユーザ用（メールアドレス認証）
###     'allauth.account.auth_backends.AuthenticationBackend',
###     ### 管理サイト用（ユーザ名認証）
###     'django.contrib.auth.backends.ModelBackend',
### )
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)
### メールアドレス認証に変更する
### ACCOUNT_AUTHENTICATION_METHOD = 'email'
### ACCOUNT_USERNAME_REQUIRED = False
### サインアップにメールアドレス確認をはさむように設定する
### ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
### ACCOUNT_EMAIL_REQUIRED = True
### ログイン、ログアウト後の遷移先を設定する
### LOGIN_REDIRECT_URL = 'diary:index'
### ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'
### ログアウトリンクのクリックでログアウトするように設定する
### ACCOUNT_LOGOUT_ON_GET = True
### django-allauthが送信するメールの件名に自動付与される接頭辞をブランクにするように設定する
### ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
### デフォルトのメール送信元を設定する
### DEFAULT_FROM_EMAIL = os.environ.get('FROM_EMAIL')

