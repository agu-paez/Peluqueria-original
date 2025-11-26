"""
Django settings for Peluqueria_Web project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
#  SEGURIDAD / ENTORNO
# ==========================

# En local, si no hay variable de entorno, usa la clave de siempre.
# En Render, le vas a pasar SECRET_KEY por Environment Variables.
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-11mkq_v4+p(k#-#8dpp+9nny0l+-#*%g#el(d_=aqg18y3!#om"
)

# En local: DEBUG=True (porque no vas a setear DEBUG en el entorno)
# En Render: ponés DEBUG=False en las variables de entorno
DEBUG = os.environ.get("DEBUG", "True") == "True"

# En local: 127.0.0.1 y localhost
# En Render: ALLOWED_HOSTS = .onrender.com
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'turnos',
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

ROOT_URLCONF = 'Peluqueria_Web.urls'

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

# Database (por ahora sqlite, para Render sirve para probar)
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

# ==========================
#  ESTÁTICOS
# ==========================

STATIC_URL = 'static/'

# dónde están tus archivos estáticos en desarrollo
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# carpeta a la que collectstatic va a copiar todo para producción (Render)
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

