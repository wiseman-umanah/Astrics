from appwrite.client import Client
from appwrite.services.storage import Storage
from appwrite.input_file import InputFile
import hashlib
from os import getenv
from space.models import FileModel


client = Client()
client.set_endpoint(getenv('BASE_URL'))
client.set_project(getenv('PROJECT_ID'))

storage = Storage(client)



def upload_file_to_appwrite(file, filename):
	result = storage.create_file(
		bucket_id = getenv('BUCKET_ID'),
		file_id = 'unique()',
		file = InputFile.from_bytes(file, filename=filename)
	)

	return result["$id"]


def delete_file_from_appwrite(file_id):
	storage.delete_file(
		bucket_id=getenv('BUCKET_ID'),
		file_id=file_id
	)


def calculate_file_hash(file):
	hasher = hashlib.sha256()
	for chunk in file.chunks():
		hasher.update(chunk)
	return hasher.hexdigest()


def cleanup_unnecessary_file(file_id):
	old_pic = FileModel.objects.filter(file_id=file_id).first()
	if old_pic:
		old_pic.reference_count -= 1
		if old_pic.reference_count <= 0:
			delete_file_from_appwrite(old_pic.file_id)
			old_pic.delete()
		else:
			old_pic.save()
			