import os

APP_PROFILE = os.getenv("APP_PROFILE", "local")
ENV_FILE = f".env.{APP_PROFILE}"
