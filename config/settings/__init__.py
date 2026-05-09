import os
from dotenv import load_dotenv
import json

load_dotenv()
try:
    print("DEBUG VALUE:", json.loads(os.getenv("DEBUG")))  # type: ignore
except TypeError:
    print("DEBUG VALUE:", "None set in .env")

if os.environ.get("ENV_NAME") == "Production":
    print("Warning: PROD ENV")
    from .production import *
elif os.environ.get("ENV_NAME") == "Staging":
    print("Warning: STAGING ENV")
    from .staging import *
else:
    print("WARNING: DEV ENV")
    from .local import *
