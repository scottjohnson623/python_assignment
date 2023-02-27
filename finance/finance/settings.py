import os
import environ
from pathlib import Path

env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env("APP_SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []

ALPHAVANTAGE_API_KEY = env("ALPHAVANTAGE_API_KEY", None)

INSTALLED_APPS = [
    "securities",
    "finance",
    "rest_framework",
    "rest_framework_json_api",
]

MIDDLEWARE = []

ROOT_URLCONF = "finance.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "finance.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": 5432,
    }
}

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "finance.pagination.CustomPagination",
    "PAGE_SIZE": 5,
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
    "EXCEPTION_HANDLER": "finance.exception_handler.custom_exception_handler",
    "UNAUTHENTICATED_USER": None,
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
