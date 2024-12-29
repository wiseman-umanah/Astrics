from django.db import models
from django.urls import reverse

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name="profile")
	profile_pic_id = models.CharField(max_length=255, blank=True, null=True)
	cover_pic_id = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.user.username

	def get_absolute_url(self):
		return reverse('profile', args=[self.user.username])
	