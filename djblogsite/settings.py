"""
Django settings for djblogsite project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment variable handling
def get_env_value(env_variable, default_value=''):
    return os.environ.get(env_variable) or os.getenv(env_variable) or default_value

# SECURITY SETTINGS
SECRET_KEY = get_env_value('SECRET_KEY')
DEBUG = get_env_value('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = get_env_value('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'widget_tweaks',
    'imagekit',
]

LOCAL_APPS = [
    'blog.apps.BlogConfig',
    'accounts.apps.AccountsConfig',
    'dashboard.apps.DashboardConfig',
    'api.apps.ApiConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djblogsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.blog_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'djblogsite.wsgi.application'

# Database Configuration
if 'VERCEL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=get_env_value('POSTGRES_URL'),
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': get_env_value('DB_NAME', 'junsproduction_db'),
            'USER': get_env_value('DB_USER', 'postgres'),
            'PASSWORD': get_env_value('DB_PASSWORD'),
            'HOST': get_env_value('DB_HOST', 'localhost'),
            'PORT': get_env_value('DB_PORT', '5432'),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
if 'VERCEL' in os.environ:
    DEFAULT_FILE_STORAGE = 'blog.storage.VercelBlobStorage'
    VERCEL_BLOB_CLIENT_TOKEN = get_env_value('BLOB_READ_WRITE_TOKEN')
    MEDIA_URL = 'https://blob.vercel-storage.com/'
else:
    MEDIA_ROOT = BASE_DIR / 'media'
    MEDIA_URL = '/media/'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_env_value('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = get_env_value('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_value('EMAIL_HOST_PASSWORD')

# Authentication
AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = get_env_value('CORS_ALLOWED_ORIGINS', '').split(',') if not DEBUG else []

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Vercel Configuration
VERCEL = bool(os.getenv('VERCEL', False))
VERCEL_BLOB_CLIENT_TOKEN = os.getenv('BLOB_READ_WRITE_TOKEN', '')

if VERCEL:
    ALLOWED_HOSTS.append('.vercel.app')
    
    # Database configuration for Vercel
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('POSTGRES_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

    # Media files with Vercel Blob
    DEFAULT_FILE_STORAGE = 'blog.storage.VercelBlobStorage'
    MEDIA_URL = 'https://blob.vercel-storage.com/'
else:
    # Local development settings
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
