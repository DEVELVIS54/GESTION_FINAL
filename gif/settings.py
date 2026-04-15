"""
Django settings for gif project.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-l+-y%0pr_@gqpvw0q@iywww65)o)znmx+6vd+@6@qaxr&pe*_l'

DEBUG = True

ALLOWED_HOSTS = ['*']  # Autorise l'accès en ligne

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'SE',  # Votre application
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Ajout pour les fichiers statiques
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Gestion des fichiers statiques
import os

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

ROOT_URLCONF = 'gif.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'gif.wsgi.application'

import dj_database_url
import os

import dj_database_url

DATABASES = {
    'default': dj_database_url.parse("postgresql://bdgestion_oj0j_user:ixOmx5hGVKOi4INSFcCBlcEjK6Drm6Ow@dpg-d7fo1h9j2pic73a2o56g-a.ohio-postgres.render.com/bdgestion_oj0j")
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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ====================
# CONFIGURATION AUTHENTIFICATION (AJOUTEZ CES 3 LIGNES)
# ====================

from django.urls import reverse_lazy

LOGIN_URL = reverse_lazy('SE/connexion')  # ← Utilise le nom de l'URL
LOGIN_REDIRECT_URL = reverse_lazy('accueil')
LOGOUT_REDIRECT_URL = reverse_lazy('connexion')