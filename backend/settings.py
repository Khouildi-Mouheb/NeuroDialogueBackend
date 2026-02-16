from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

AUTH_USER_MODEL = os.getenv("AUTH_USER_MODEL")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

import os
from dotenv import load_dotenv

load_dotenv()

# FastAPI Configuration
FASTAPI_URL = os.getenv('FASTAPI_URL', 'http://localhost:8000/chat')

# Log the URL on startup (for debugging)
print(f"🔗 FastAPI URL configured: {FASTAPI_URL}")


AUTHENTICATION_BACKENDS=[
    "django.contrib.auth.backends.ModelBackend",
    
]

LOGIN_URL = "login"
LOGIN_REDIRECTED_URL="home"
LOGOUT_REDIRECTED_URL="home"







# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG") == "True"

SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE") == "True"
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE") == "True"

CSRF_TRUSTED_ORIGINS = [
    'https://neurodialoguebackend-production.up.railway.app',
    'https://*.railway.app',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:8001',
    'http://127.0.0.1:8001',
]

# Application definition

INSTALLED_APPS = [
    'users',
    'chat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
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

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"

 # Local needs this

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_NAME_RAILWAY"),
        "USER": os.getenv("USER_RAILWAY"),
        "PASSWORD": os.getenv("PASSWORD_RAILWAY"),
        "HOST": os.getenv("DB_HOST_RAILWAY"), 
        "PORT": os.getenv("PORT_RAILWAY"),
    }
}



# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
