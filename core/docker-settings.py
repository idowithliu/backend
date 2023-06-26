from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ["localhost"]

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
MEDIA_ROOT = "/app-media"
MEDIA_URL = "/media/"

STATIC_ROOT = "/static"
STATIC_URL = "/static/"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "idowithliu",
        "USER": "idowithliu_postgres_user",
        "PASSWORD": "idowithliu_postgres_password",
        "HOST": "postgres",
        "PORT": "",
    }
}

try:
    with open(os.path.join(os.path.dirname(__file__), "docker-config.py")) as f:
        exec(f.read(), globals())
except IOError:
    raise TypeError(
        "Please create a config.py file to override values in settings.py and docker-settings.py"
    )
