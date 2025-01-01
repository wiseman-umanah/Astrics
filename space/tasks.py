from celery import shared_task
from . models import FileModel
from utils.files import cleanup_unnecessary_file
from utils.emails import notify_admins


@shared_task
def cleanup_files():
	orphan_files = FileModel.objects.filter(reference_count__lte=0)
	for file in orphan_files:
		try:
			cleanup_unnecessary_file(file.file_id)
			file.delete()
		except Exception as error:
			notify_admins(str(error))
