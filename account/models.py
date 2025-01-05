from django.db import models
from django.urls import reverse

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name="profile")
	profile_pic_id = models.CharField(max_length=255, blank=True, null=True)
	cover_pic_id = models.CharField(max_length=255, blank=True, null=True)
	follows = models.ManyToManyField(
		"self",
		related_name="followed_by",
		symmetrical=False,
		blank=True
	)

	def __str__(self):
		return self.user.username

	def get_absolute_url(self):
		return reverse('profile', args=[self.user.username])


class Post(models.Model):
	MEDIA_CHOICES = [
		('image', 'Image'),
		('video', 'Video'),
		('text', 'Text')
	]
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="posts")
	title = models.CharField(max_length=255, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	file_id = models.CharField(max_length=255, null=True)
	media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']
	
	def __str__(self):
		return f'Post with id {self.id} created by user {self.user.username}'

	def get_absolute_url(self):
		pass