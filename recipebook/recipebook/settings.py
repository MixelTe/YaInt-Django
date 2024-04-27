import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv


def load_bool_from_env(key: str, default: bool) -> bool:
    strv = os.environ.get(key, str(default)).lower().strip()
    if strv == "":
        return default

    return strv in ["true", "t", "yes", "y", "1"]


def load_int_from_env(key: str, default: int) -> int:
    value = os.environ.get(key, "")
    if value.isdigit():
        return int(value)

    return default


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "not_secret_key")

DEBUG = load_bool_from_env("DJANGO_DEBUG", False)
DEFAULT_USER_IS_ACTIVE = load_bool_from_env("DEFAULT_USER_IS_ACTIVE", DEBUG)
MAX_AUTH_ATTEMPTS = load_int_from_env("MAX_AUTH_ATTEMPTS", 5)

DJANGO_ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*")
ALLOWED_HOSTS = list(map(str.strip, DJANGO_ALLOWED_HOSTS.split(",")))

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core.apps.CoreConfig",
    "feedback.apps.FeedbackConfig",
    "recipes.apps.RecipesConfig",
    "users.apps.UsersConfig",
    "sorl.thumbnail",
    "django_cleanup.apps.CleanupConfig",
    "mdeditor",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_URLCONF = "recipebook.urls"

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

WSGI_APPLICATION = "recipebook.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".NumericPasswordValidator"
        ),
    },
]

AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = [
    "users.backends.AuthenticationBackend",
]

LOGIN_URL = "/users/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

LANGUAGE_CODE = "ru"

LANGUAGES = [
    ("ru", _("Russian")),
    ("en", _("English")),
]

TIME_ZONE = "UTC"

USE_I18N = True

LOCALE_PATHS = (BASE_DIR / "locale/",)

USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "send_mail"
DEFAULT_FROM_EMAIL = os.environ.get("DJANGO_MAIL", "webmaster@localhost")

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

UPLOADS_ROOT = BASE_DIR / "uploads"

X_FRAME_OPTIONS = "SAMEORIGIN"

MDEDITOR_CONFIGS = {
    "default": {
        "width": "100% ",
        "height": 500,
        "toolbar": [
            "undo",
            "redo",
            "|",
            "bold",
            "del",
            "italic",
            "quote",
            "ucwords",
            "uppercase",
            "lowercase",
            "|",
            "h1",
            "h2",
            "h3",
            "h5",
            "h6",
            "|",
            "list-ul",
            "list-ol",
            "hr",
            "|",
            "link",
            "reference-link",
            "image",
            "code",
            "preformatted-text",
            "code-block",
            "table",
            "datetime",
            "emoji",
            "html-entities",
            "pagebreak",
            "goto-line",
            "|",
            "help",
            "info",
            "||",
            "preview",
            "watch",
            "fullscreen",
        ],
        "upload_image_formats": [
            "jpg",
            "jpeg",
            "gif",
            "png",
            "bmp",
            "webp",
            "svg",
        ],
        "image_folder": "editor",
        "theme": "default",  # dark / default
        "preview_theme": "default",  # dark / default
        "editor_theme": "default",  # pastel-on-dark / default
        "toolbar_autofixed": False,
        "search_replace": True,
        "emoji": True,
        "tex": True,
        "flow_chart": True,
        "sequence": True,
        "watch": True,
        "lineWrapping": True,
        "lineNumbers": True,
        "language": "en",  # zh / en / es
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "debug.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": True,
        },
    },
}

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
else:
    if SECRET_KEY == "not_secret_key":
        import logging

        logging.warning("Secret key is not set in product mode")


__all__ = []
