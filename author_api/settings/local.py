from .base import * #nqoa
from .base import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default ="_uzaBYHBlv0a8H8GikhlUiXic0gdI8c9BSU-Ly9jr1bOqPkQXjY"
)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8080']
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

