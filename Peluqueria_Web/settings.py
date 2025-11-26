"""
Django settings for Peluqueria_Web project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# =======================
#  SECURITY / ENVIRONMENT
# =======================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-11mkq_v4+p(k#-#8dpp+9nny0l+-#*%g#el(d_=aqg18y3!#om"
)

DEBUG = os.environ.get("DEBUG", "True") == "True"

# para asegurarnos que Render funcione:
ALLOWED_HOSTS = ["*"]   # luego lo ajustamos, pero así FUNCIONA seguro


# =======================
#      APPLICATIONS
# =======================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'turnos',
]

# =======================
#       MIDDLEWARE
# =======================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise para servir archivos estáticos en producción
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Peluqueria_Web.urls'

# =======================
#       TEMPLATES
# =======================

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

WSGI_APPLICATION = 'Peluqueria_Web.wsgi.application'


# =======================
#     DATABASE (sqlite)
# =======================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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


LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Buenos_Aires'
USE_I18N = True
USE_TZ = True


# =======================
#      STATIC FILES
# =======================

STATIC_URL = 'static/'

# Carpeta de desarrollo
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Carpeta a la que collectstatic exporta en producción
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise storage (archivos comprimidos/caché)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
