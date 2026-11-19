import os

BASE_URL = os.getenv("BASE_URL")

APP_USERNAME = os.getenv("APP_USERNAME", "admin")
APP_PASSWORD = os.getenv("APP_PASSWORD", "admin123")

BROWSER = os.getenv("BROWSER", "chromium")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

DEFAULT_TIMEOUT = int(
    os.getenv("DEFAULT_TIMEOUT", "10000")
)