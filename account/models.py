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
		return reverse('space:user-profile', args=[self.user.username])


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
		return reverse('space:view-post', args=[self.user.username, self.id])

	def is_liked_by(self, user):
		return self.likes.filter(user=user).exist()


class Like(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="liked_posts")
	liked_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('post', 'user', )


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="commented_posts")
	content = models.TextField()
	comment_on = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('post', 'user')
		ordering = ('-comment_on',)


class Favorite(models.Model):
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="favorites")
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	favorite_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('post', 'user')
		ordering = ('-favorite_at',)
