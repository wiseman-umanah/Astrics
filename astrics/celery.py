import os 
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "astrics.settings")
app = Celery("astrics")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.beat_schedule = {
	'fetch-daily-content': {
        'task': 'system.tasks.fetch_daily_content',
        'schedule': crontab(hour='8', minute='0'),
    },
	'cleanup_unused_files': {
		'task': 'space.tasks.cleanup_files',
		'schedule': crontab(0, 0,
					  day_of_month='1',
					  month_of_year='*')
	}
}
