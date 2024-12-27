from django.db import models

class FileModel(models.Model):
	file_id = models.CharField(max_length=255, unique=True)
	hash = models.CharField(max_length=64, unique=True)
	reference_count = models.IntegerField(default=0)
	
