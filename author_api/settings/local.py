from .base import * #nqoa
from .base import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default ="_uzaBYHBlv0a8H8GikhlUiXic0gdI8c9BSU-Ly9jr1bOqPkQXjY"
)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

ALLOWED_HOSTS = []