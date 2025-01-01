import os 
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "astrics.settings")
app = Celery("astrics")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
# app.conf.beat_schedule = {
# 	'test': {
# 		'task': 'system.tasks.test', replace with fetch image task
# 		'schedule': 5, - set time to every 1 am 
# 	},
# } run with celery -A astrics beat,start worker celery -A astrics worker
