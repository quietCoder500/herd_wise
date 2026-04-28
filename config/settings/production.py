from config.settings.base import *  # noqa: F403
import sentry_sdk

DEBUG = False

sentry_sdk.init(
    dsn="https://4885793cd48420f76ecdd83a5bca99a3@o4506668046614528.ingest.us.sentry.io/4511215957245952",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)
