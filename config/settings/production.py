from config.settings.base import *  # noqa: F403
import sentry_sdk

DEBUG = False

sentry_sdk.init(
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)
