from config.settings.base import *  # noqa: F403

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    # },
]


INSTALLED_APPS.append("django_extensions")  # noqa: F405

# Browser reload
INSTALLED_APPS.append("django_browser_reload")  # noqa: F405
MIDDLEWARE.insert(0, "django_browser_reload.middleware.BrowserReloadMiddleware")  # noqa: F405

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

ALLOWED_HOSTS.append("127.0.0.1")  # noqa: F405

MEDIA_ROOT = BASE_DIR / "media"  # noqa: F405
MEDIA_URL = "/media/"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
