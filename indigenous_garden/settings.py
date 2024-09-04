"""
Django settings for indigenous_garden project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from environ import FileAwareEnv
from glob import glob
from dotenv import load_dotenv, find_dotenv

env = FileAwareEnv()
load_dotenv(find_dotenv())

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Absolute upload file directory
# https://docs.djangoproject.com/en/4.2/ref/settings/#media-root
MEDIA_ROOT = '/media'

STATIC_ROOT = BASE_DIR / 'static/'

STATICFILES_DIRS = [
    ('bootstrap', BASE_DIR / "node_modules/bootstrap/dist"),
    ('bootstrap-icons', BASE_DIR / "node_modules/bootstrap-icons"),
    ('fontawesome', BASE_DIR / "node_modules/@fortawesome/fontawesome-free"),
    ('ol', BASE_DIR / "node_modules/ol"),
    ('video.js', BASE_DIR / "node_modules/video.js"),
    ('videojs-vr', BASE_DIR / "node_modules/videojs-vr"),
    ('img-comparison-slider', BASE_DIR / "node_modules/img-comparison-slider"),
    '/static-assets',
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-0lgov2k26n+=bjocstuna-@888$&g3(xvxugltqd*xx+z=_p1=')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])


# Application definition

INSTALLED_APPS = [
    'garden.apps.GardenConfig',
    'django_admin_kubi',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'constrainedfilefield',
    'health_check',
    'django_cleanup.apps.CleanupConfig',
    'kp_static_version',
    'admin_async_upload',
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

ROOT_URLCONF = 'indigenous_garden.urls'

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

WSGI_APPLICATION = 'indigenous_garden.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env('DB_HOST', default=''),
        'NAME': env('DB_NAME', default=''),
        'USER': env('DB_USER', default=''),
        'PASSWORD': env('DB_PASSWORD', default=''),
        'PORT': env.int('DB_PORT', default=5432),
    }
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

TIME_ZONE = 'America/Vancouver'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Uploaded files (Audio, Images)
# https://docs.djangoproject.com/en/4.2/ref/settings/#media-url
MEDIA_URL = 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# default upload permissions
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
FILE_UPLOAD_PERMISSIONS = 0o644

# email host
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_PORT = env.int('EMAIL_PORT', default=1025)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')


DJANGO_ADMIN_KUBI = {
    'ADMIN_HISTORY': True,  # enables the history action panel
    # 'ADMIN_SEARCH': True,  # enables a full modal search
}

# CSRF form settings
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=['http://localhost:8080'])

# iframe settings
X_FRAME_OPTIONS = "SAMEORIGIN"


DATA_UPLOAD_MAX_MEMORY_SIZE = 256 * 1024 * 1024 # 256MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 256 * 1024 * 1024 # 256MB

# logout redirection
LOGOUT_REDIRECT_URL = 'admin:login'

# add versions to static assets
KP_STATIC_VERSION = env('GIT_COMMIT_SHORT', default='')