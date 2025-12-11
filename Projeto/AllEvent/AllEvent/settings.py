"""
Django settings for AllEvent project.
"""
import dj_database_url
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-sp063i^kdyy^)-$l=0ar2w#()h#^&$-*u3bl_*$4q)@vx-g2w$"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'AllEvent',
    'core.apps.CoreConfig',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", 
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "AllEvent.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'AllEvent' / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "AllEvent.wsgi.application"



DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

database_url = os.environ.get("DATABASE_URL")
if database_url:
    DATABASES["default"] = dj_database_url.parse(database_url)


AUTH_PASSWORD_VALIDATORS = [
    { "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator" },
    { "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator" },
    { "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator" },
    { "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator" },
]


LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo" 
USE_I18N = True
USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = [
    BASE_DIR / 'AllEvent' / 'static'
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = '/' 
LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = 'login' 

CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',  
    'https://allevent-site.onrender.com', 
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]



MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = 30


EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


DEFAULT_FROM_EMAIL = 'allevent06@gmail.com'