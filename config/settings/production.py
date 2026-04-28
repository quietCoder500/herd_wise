from config.settings.base import *  # noqa: F403
import sentry_sdk

sentry_sdk.init(
    dsn=env("SENTRY_DSN"),  # noqa: F405 # type: ignore
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)
