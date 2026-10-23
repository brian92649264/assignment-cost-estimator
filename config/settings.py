import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY") or get_random_secret_key()

DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "estimator",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {}

LANGUAGE_CODE = "en-gb"
USE_I18N = False

STATIC_URL = "static/"
