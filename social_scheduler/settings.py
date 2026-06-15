"""
Configurações globais do projeto PostFlow (social_scheduler).
"""
import os
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]),
)

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY", default="django-insecure-dev-key-change-in-production")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_q",
    "accounts",
    "scheduler",
    "integrations",
    "logs",
    "notifications",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "logs.middleware.AuditLogMiddleware",
]

ROOT_URLCONF = "social_scheduler.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "social_scheduler.wsgi.application"

DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="sqlite:///db.sqlite3",
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.CustomUser"

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "accounts:login"

# Criptografia de tokens OAuth
SOCIAL_ENCRYPTION_KEY = env("SOCIAL_ENCRYPTION_KEY", default="")

# Django Q2 — broker via ORM (sem Redis)
Q_CLUSTER = {
    "name": "postflow",
    "workers": 2,
    "recycle": 500,
    "timeout": 300,
    "retry": 360,
    "queue_limit": 50,
    "bulk": 10,
    "orm": "default",
    "catch_up": False,
    "save_limit": 250,
    "ack_failures": True,
}

# E-mail
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@postflow.app")

# OAuth — credenciais das redes sociais
FACEBOOK_APP_ID = env("FACEBOOK_APP_ID", default="")
FACEBOOK_APP_SECRET = env("FACEBOOK_APP_SECRET", default="")
INSTAGRAM_APP_ID = env("INSTAGRAM_APP_ID", default="")
INSTAGRAM_APP_SECRET = env("INSTAGRAM_APP_SECRET", default="")
LINKEDIN_CLIENT_ID = env("LINKEDIN_CLIENT_ID", default="")
LINKEDIN_CLIENT_SECRET = env("LINKEDIN_CLIENT_SECRET", default="")
TWITTER_CLIENT_ID = env("TWITTER_CLIENT_ID", default="")
TWITTER_CLIENT_SECRET = env("TWITTER_CLIENT_SECRET", default="")
