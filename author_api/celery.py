import os
from celery import Celery
from django.conf import settings

#TODO: change this in production

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "author_api.settings.local")

app = Celery('author_api', broker="redis://127.0.0.1:6379", backend="redis://127.0.0.1:6379")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
