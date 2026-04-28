from config.settings.base import *  # noqa: F403
import sentry_sdk
import os

sentry_sdk.init(
    dsn=str(os.getenv("SENTRY_DSN")),  # noqa: F405 # type: ignore
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)
