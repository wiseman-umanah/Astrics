from django.db import models
from datetime import date
from django.contrib.postgres.search import SearchVectorField


# Create your models here.
class AstricsModel(models.Model):
	MEDIA_CHOICES = [
		('image', 'Image'),
		('video', 'Video'),
	]
	date = models.DateField(default=date.today, unique=True)
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	url = models.URLField()
	media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES)
	created_at = models.DateTimeField(auto_now_add=True)
	search_vector = SearchVectorField(null=True)
	
	def __str__(self):
		return f'{self.title}: {self.url}'

	class Meta:
		ordering = ('-date',)
