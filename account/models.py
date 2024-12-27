from django.db import models
# from django.contrib.auth.models import User


# # Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
	profile_pic = models.CharField(max_length=255, blank=True, null=True)
	cover_pic = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.user.username
