import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "csv_processor.settings")
app = Celery("csv_processor")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()