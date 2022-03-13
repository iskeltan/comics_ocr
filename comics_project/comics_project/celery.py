import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comics_project.settings')

from django.conf import settings

app = Celery("comics_project")

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug(self):
    print("request: {0!r}".format(self.request))